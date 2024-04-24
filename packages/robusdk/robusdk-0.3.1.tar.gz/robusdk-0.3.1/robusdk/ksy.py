#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kaitaistruct import KaitaiStream

def ksy(type, node):
    async def parse(payload):
        return payload
        # const code = await KaitaiStructCompiler().compile('python', jsYaml.load(FileIO(`ksy/ec/${type}/nodes/${node}.ksy`)))
        # const Parser = requireFromString(Object.values(code).join('\n'))
        # return sanitize(Parser(KaitaiStream(payload)))

    return parse
