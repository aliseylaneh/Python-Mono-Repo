import asyncio
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast
from .unicode_finder_fastapi.services import InvertedIndex, format_results

CRLF = b"\r\n"
PROMPT = b"?>"


async def search(query: str, index: InvertedIndex, writer: asyncio.StreamWriter):
    chars = index.search(query)
    lines = (line.encode() + CRLF for line in format_results(chars))
    writer.writelines(lines)
    await writer.drain()
    status_line = f'{"-"*66} {len(chars)} found'
    writer.write(status_line.encode() + CRLF)
    return len(chars)


async def finder(
    index: InvertedIndex, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    client = writer.get_extra_info("peername")
    while True:
        writer.write(PROMPT)
        await writer.drain()
        data = await reader.readline()
        if not data:
            break
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = "\x00"
        print(f"From {client}: {query!r}")
        if query:
            if ord(query[:1]) < 32:
                break
            result = await search(query, index, writer)
            print(f" To {client}: {result} results.")
        writer.close()
        await writer.wait_closed()
        print(f"Close {client}")


async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    server = await asyncio.start_server(functools.partial(finder, index), host, port)
    socket_list = cast(tuple[TransportSocket, ...], server.sockets)
    addr = socket_list[0].getsockbyname()
    print(f"Serving on {addr}. Hit")
    await server.serve_forever()


def main(host: str = "127.0.0.1", port_arg: str = "2323"):
    port = int(port_arg)
    print("Building index.")
    index = InvertedIndex()
    try:
        asyncio.run(supervisor(index=index, host=host, port=port))
    except KeyboardInterrupt:
        print("\nServer shut down.")


if __name__ == "__main__":
    main(*sys.argv[1:])
