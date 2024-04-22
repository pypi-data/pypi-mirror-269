import argparse
import time

from DLMS_SPODES_client.servers import TransactionServer, Result
from DLMS_SPODES_client import task, services
from DLMS_SPODES_client.client import Client, logL, IDFactory
from DLMS_SPODES_communications import AsyncSerial, AsyncNetwork


id_factory = IDFactory("#")


def main():
    parser = argparse.ArgumentParser(
        description="Update Firmware Program for DLMS meters")
    parser.add_argument(
        '-t', '--type',
        choices=("File", "Serial", "Net"),
        required=True,
        help="Communication type")
    parser.add_argument(
        "-p",
        nargs='*',
        help="connection parameters")
    parser.add_argument(
        "-T", "--timeout",
        type=int,
        default=60,
        help="communication timeout")
    parser.add_argument(
        "-s", "--secret",
        type=lambda value: str.encode(value, "ascii"),
        default="0000000000000000",
        help="DLMS association secret")
    parser.add_argument(
        "-sap",
        type=int,
        default=0x30,
        help="DLMS SAP")
    parser.add_argument(
        "-da",
        type=int,
        default=0x10,
        help="DLMS Device Address")
    parser.add_argument(
        "-m", "--mechanism_id",
        type=int,
        default=2,
        help="DLMS association mechanism ID")
    parser.add_argument(
        "-as", "--addr_size",
        type=int,
        choices=(-1, 1, 2, 4),
        default=1,
        help="Client HDLC address size type from :-1, 1, 2, 4")
    parser.add_argument(
        "-d", "--loop_delay",
        nargs='*',
        type=int,
        default=2,
        help="delay between attempts of loop(in second)")
    parser.add_argument(
        "-l", "--n_loops",
        nargs='*',
        type=int,
        default=3,
        help="attempts amount")
    parser.add_argument(
        "-f", "--file",
        type=str,
        default=".//output.txt",
        help="output result file"
    )
    args = parser.parse_args()
    if (source := args.type) in ("Serial", "Net"):
        clients = [c := Client(
                        SAP=args.sap,
                        secret=args.secret.hex(),
                        addr_size=-1,
                        id_=id_factory.create())]
        c.m_id.set(args.mechanism_id)
        c.device_address.set(args.da)
        c_t = AsyncSerial if source == "Serial" else AsyncNetwork
        c.media = c_t(*args.p)
        c.media.inactivity_timeout = args.timeout
    elif source == "File":
        if len(args.p) == 1:
            clients = services.get_client_from_csv(
                file_name=args.p[0],
                id_factory=id_factory)
        else:
            raise ValueError("-p for \"File\" must have 1 file name")
    else:
         raise ValueError(F"unknown {source=}")
    t_server = TransactionServer(
        clients=clients,
        tsk=task.Loop(
            task=task.UpdateFirmware(),
            func=lambda res: res,
            delay=args.loop_delay,
            attempt_amount=args.n_loops
        )
    )
    t_server.start()
    results = list(t_server.results)
    with open(
            file=args.file,
            mode="w+",
            encoding="utf-8") as file:
        while results:
            time.sleep(3)
            for res in results:
                res: Result
                if res.complete:
                    results.remove(res)
                    res.client.log(logL.INFO, F"Для {res.client} обновление: {'Удачно' if res.value else 'Неудачно'}")
                    file.write(F"{res.client} {res.value}")


if __name__ == "__main__":
    main()
