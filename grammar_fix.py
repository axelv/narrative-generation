from __future__ import annotations

import sys


from typing import TYPE_CHECKING
from typing import Optional
from typing import TextIO

from liquid.ast import Node
from liquid.ast import BlockNode

from liquid.context import Context

from liquid.parse import expect
from liquid.parse import get_parser

from liquid.stream import TokenStream
from liquid.tag import Tag

from liquid.token import TOKEN_EXPRESSION, Token
from liquid.token import TOKEN_TAG
from liquid.token import TOKEN_TRUE
from liquid.token import TOKEN_FALSE
from liquid.token import TOKEN_NIL
from liquid.token import TOKEN_NULL
from liquid.token import TOKEN_AS
from liquid.token import TOKEN_EOF


if TYPE_CHECKING:
    from liquid import Environment

TAG_FIX = sys.intern("fix")
TAG_ENDFIX = sys.intern("endfix")

with_expression_keywords = frozenset(
    [
        TOKEN_TRUE,
        TOKEN_FALSE,
        TOKEN_NIL,
        TOKEN_NULL,
        TOKEN_AS,
    ]
)

class FixNode(Node):
    def __init__(self, tok: Token, block: BlockNode):
        self.tok = tok
        self.block = block

    def render_to_output(self, context: Context, buffer: TextIO) -> Optional[bool]:
        self.block.render(context, buffer)

    async def render_to_output_async(self, context: Context, buffer: TextIO) -> Optional[bool]:
        return await super().render_to_output_async(context, buffer)


class FixGrammar(Tag):
    name = TAG_FIX
    end = TAG_ENDFIX

    def __init__(self, env: Environment):
        super().__init__(env=env)
        self.parser = get_parser(self.env)

    def parse(self, stream: TokenStream) -> Node:
        expect(stream, TOKEN_TAG, value=TAG_FIX)
        tok = stream.current

        stream.next_token()
        expect(stream, TOKEN_EXPRESSION)
        identifier = stream.current.value
        assert identifier == "grammar"
        stream.next_token()
        block = self.parser.parse_block(stream, (TAG_ENDFIX, TOKEN_EOF))
        expect(stream, TOKEN_TAG, value=TAG_ENDFIX)

        return FixNode(tok=tok, block=block)
