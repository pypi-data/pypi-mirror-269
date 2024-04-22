from pathlib import Path
from typing import Callable, Iterable, Iterator, List, Optional, Tuple

from thinc.api import (
    Linear,
    Maxout,
    Model,
    Ragged,
    chain,
    list2ragged,
    reduce_mean,
    residual,
    tuplify,
)
from thinc.types import Floats2d

from ...errors import Errors
from ...kb import Candidate, InMemoryLookupKB, KnowledgeBase
from ...tokens import Doc, Span, SpanGroup
from ...util import registry
from ...vocab import Vocab
from ..extract_spans import extract_spans

CandidatesForMentionT = Iterable[Candidate]
CandidatesForDocT = Iterable[CandidatesForMentionT]


@registry.architectures("spacy.EntityLinker.v2")
def build_nel_encoder(
    tok2vec: Model, nO: Optional[int] = None
) -> Model[List[Doc], Floats2d]:
    with Model.define_operators({">>": chain, "&": tuplify}):
        token_width = tok2vec.maybe_get_dim("nO")
        output_layer = Linear(nO=nO, nI=token_width)
        model = (
            ((tok2vec >> list2ragged()) & build_span_maker())
            >> extract_spans()
            >> reduce_mean()
            >> residual(Maxout(nO=token_width, nI=token_width, nP=2, dropout=0.0))  # type: ignore
            >> output_layer
        )
        model.set_ref("output_layer", output_layer)
        model.set_ref("tok2vec", tok2vec)
    # flag to show this isn't legacy
    model.attrs["include_span_maker"] = True
    return model


def build_span_maker(n_sents: int = 0) -> Model:
    model: Model = Model("span_maker", forward=span_maker_forward)
    model.attrs["n_sents"] = n_sents
    return model


def span_maker_forward(model, docs: List[Doc], is_train) -> Tuple[Ragged, Callable]:
    ops = model.ops
    n_sents = model.attrs["n_sents"]
    candidates = []
    for doc in docs:
        cands = []
        try:
            sentences = [s for s in doc.sents]
        except ValueError:
            # no sentence info, normal in initialization
            for tok in doc:
                tok.is_sent_start = tok.i == 0
            sentences = [doc[:]]
        for ent in doc.ents:
            try:
                # find the sentence in the list of sentences.
                sent_index = sentences.index(ent.sent)
            except AttributeError:
                # Catch the exception when ent.sent is None and provide a user-friendly warning
                raise RuntimeError(Errors.E030) from None
            # get n previous sentences, if there are any
            start_sentence = max(0, sent_index - n_sents)
            # get n posterior sentences, or as many < n as there are
            end_sentence = min(len(sentences) - 1, sent_index + n_sents)
            # get token positions
            start_token = sentences[start_sentence].start
            end_token = sentences[end_sentence].end
            # save positions for extraction
            cands.append((start_token, end_token))

        candidates.append(ops.asarray2i(cands))
    lengths = model.ops.asarray1i([len(cands) for cands in candidates])
    out = Ragged(model.ops.flatten(candidates), lengths)
    # because this is just rearranging docs, the backprop does nothing
    return out, lambda x: []


@registry.misc("spacy.KBFromFile.v1")
def load_kb(
    kb_path: Path,
) -> Callable[[Vocab], KnowledgeBase]:
    def kb_from_file(vocab: Vocab):
        kb = InMemoryLookupKB(vocab, entity_vector_length=1)
        kb.from_disk(kb_path)
        return kb

    return kb_from_file


@registry.misc("spacy.EmptyKB.v2")
def empty_kb_for_config() -> Callable[[Vocab, int], KnowledgeBase]:
    def empty_kb_factory(vocab: Vocab, entity_vector_length: int):
        return InMemoryLookupKB(vocab=vocab, entity_vector_length=entity_vector_length)

    return empty_kb_factory


@registry.misc("spacy.EmptyKB.v1")
def empty_kb(
    entity_vector_length: int,
) -> Callable[[Vocab], KnowledgeBase]:
    def empty_kb_factory(vocab: Vocab):
        return InMemoryLookupKB(vocab=vocab, entity_vector_length=entity_vector_length)

    return empty_kb_factory


@registry.misc("spacy.CandidateGenerator.v1")
def create_get_candidates() -> Callable[[KnowledgeBase, Span], Iterable[Candidate]]:
    return get_candidates


@registry.misc("spacy.CandidateGenerator.v2")
def create_get_candidates_v2() -> Callable[
    [KnowledgeBase, Iterator[SpanGroup]], Iterator[CandidatesForDocT]
]:
    return get_candidates_v2


def get_candidates(kb: KnowledgeBase, mention: Span) -> Iterable[Candidate]:
    """
    Return candidate entities for the given mention from the KB.
    kb (KnowledgeBase): Knowledge base to query.
    mention (Span): Entity mention.
    RETURNS (Iterable[Candidate]): Identified candidates for specified mention.
    """
    cands_per_doc = next(
        get_candidates_v2(kb, iter([SpanGroup(mention.doc, spans=[mention])]))
    )
    assert isinstance(cands_per_doc, list)
    return next(cands_per_doc[0])


def get_candidates_v2(
    kb: KnowledgeBase, mentions: Iterator[SpanGroup]
) -> Iterator[Iterable[Iterable[Candidate]]]:
    """
    Return candidate entities for the given mentions from the KB.
    kb (KnowledgeBase): Knowledge base to query.
    mentions (Iterator[SpanGroup]): Mentions per doc.
    RETURNS (Iterator[Iterable[Iterable[Candidate]]]): Identified candidates per mentions in document/SpanGroup.
    """
    return kb.get_candidates(mentions)
