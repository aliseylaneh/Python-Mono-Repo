import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path
import httpx
from tqdm import tqdm
from captures_flags import BASE_URL
from flag_common import main, DownloadStatus, save_flag

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str) -> bytes:
    url = f"{base_url}/{cc}/{cc}.gif".lower()
    response = await client.get(url, timeout=3.1, follow_redirects=True)
    response.raise_for_status()
    return response.content


async def download_one(
    client: httpx.AsyncClient,
    cc: str,
    base_url: str,
    semaphore: asyncio.Semaphore,
    verbose: bool,
):
    try:
        async with semaphore:
            image = await get_flag(client=client, base_url=base_url, cc=cc)
    except httpx.HTTPStatusError as e:
        response = e.response
        if response.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f"res: {response.url}"
    else:
        await asyncio.to_thread(save_flag, image, f"{cc}.gif")
        status = DownloadStatus.OK
        msg = "OK"
    if verbose and msg:
        print(cc, msg)
    return status


async def supervisor(
    cc_list: list[str], base_url: str, verbose: bool, concur_req: int
) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(value=concur_req)
    async with httpx.AsyncClient() as client:
        to_do = [
            download_one(
                client=client,
                cc=cc,
                base_url=base_url,
                semaphore=semaphore,
                verbose=verbose,
            )
            for cc in sorted(cc_list)
        ]
        to_do_iter = asyncio.as_completed(to_do)
        if not verbose:
            to_do_iter = tqdm(to_do_iter, total=len(cc_list))
            error: httpx.HTTPError | None = None
            for coro in to_do_iter:
                try:
                    status = await coro
                except httpx.HTTPStatusError as e:
                    error_msg = f"HTTP error {e.response} - {e.reason_phrase}"
                    error = e
                except httpx.RequestError as e:
                    error_msg = f"{e} {type(e)}".strip
                    error = e
                except KeyboardInterrupt:
                    break
                if error:
                    status = DownloadStatus.ERROR
                    if verbose:
                        url = str(error.request.url)
                        cc = Path(url).stem.upper()
                        print(f"{cc} error: {error_msg}")
                counter[status] += 1
    return counter


def download_many(
    cc_list: list[str], base_url: str, verbose: bool, concur_req: int
) -> Counter[DownloadStatus]:
    coro = supervisor(
        cc_list=cc_list, base_url=BASE_URL, verbose=verbose, concur_req=concur_req
    )
    counter = asyncio.run(coro)
    return counter


if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
