import argparse
import datetime
import json
import platform
import re
import subprocess
import time
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore

GatewayInfo = Tuple[str, dict[str, bool]]
GatewayMapping = Dict[int, List[GatewayInfo]]
DefaultGateway = Dict[int, GatewayInfo]
GatewaysResult = Dict[Union[int, str], Union[GatewayMapping, DefaultGateway]]


def get_default_gateway() -> str:
    """Get the default gateway IP for the active network interface."""
    try:
        import netifaces  # type: ignore
        gateways: GatewaysResult = netifaces.gateways() # type: ignore
        interface: int = netifaces.AF_INET # type: ignore
        default: Union[GatewayInfo, str] = gateways['default'][interface][0]  # type: ignore
        if isinstance(default, str):
            default_gateway: str = default
        else:
            default_gateway = default[0] # type: ignore
        return default_gateway # type: ignore
    except (KeyError, ModuleNotFoundError, ImportError):
        print("Could not determine the default gateway.")
        return '127.0.0.1'


class PingResult:
    def __init__(self, target: str, timestamp: float, response_time: Optional[float]):
        super().__init__()
        self.target = target
        self.timestamp = timestamp
        self.response_time = response_time

    def __repr__(self) -> str:
        return f"<PingResult target={self.target} timestamp={self.timestamp} response_time={self.response_time}>"

def execute_ping(target: str) -> Tuple[str, int]:
    """Executes a ping command based on the operating system."""
    ping_command = ["ping", "-n", "1", target] if platform.system() == "Windows" else ["ping", "-c", "1", target]
    process = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = process.communicate()
    return out, process.returncode

def process_ping_output(target: str, out: str, current_time: float) -> None:
    """Process the output of a ping command."""
    match = re.search(r"time[=<](\d+)ms", out)
    if match:
        time_taken = float(match.group(1))
        write_to_json(PingResult(target, current_time, time_taken))
    else:
        print(f"Failed to extract ping time from output for {target}")
        write_to_json(PingResult(target, current_time, None))

def write_to_json(result: PingResult) -> None:
    """Writes a single PingResult to a JSON lines file. Appends to the file if it exists."""
    filename = "ping_results.jsonl"
    with open(filename, 'a') as jsonfile:
        jsonfile.write(json.dumps(result.__dict__) + '\n')

def ping_targets(targets: List[str], number_of_pings: int, interval_seconds: int, duration_minutes: int) -> None:
    """Pings multiple targets a specified number of times at regular intervals for a set duration and stores results in a JSON lines file."""
    print(f"Running test for {duration_minutes} minutes with {len(targets)} destinations...")
    end_time = time.time() + duration_minutes * 60

    while time.time() < end_time:
        current_time = time.time()
        for target in targets:
            for _ in range(number_of_pings):
                out, returncode = execute_ping(target)
                if returncode == 0:
                    process_ping_output(target, out, current_time)
                else:
                    write_to_json(PingResult(target, current_time, None))
        time.sleep(interval_seconds)
    plot_from_json()

def plot_from_json(filename: str = "ping_results.jsonl") -> None:
    """Plots the ping results from a JSON file using Seaborn."""
    results: dict[str, list[PingResult]] = {}
    with open(filename, 'r') as jsonfile:
        for line in jsonfile:
            result_dict = json.loads(line)
            result = PingResult(**result_dict)
            results.setdefault(result.target, []).append(result)
    plot_ping_results(results)

def plot_ping_results(results: dict[str, list[PingResult]]) -> None:
    """Plots the ping results using Seaborn."""
    sns.set_theme(style="whitegrid") # type: ignore
    plt.figure(figsize=(12, 6)) # type: ignore
    for target, ping_results in results.items():
        times = [result.timestamp for result in ping_results if result.response_time is not None]
        pings = [result.response_time for result in ping_results if result.response_time is not None]
        sns.lineplot(x=times, y=pings, marker='o', label=f'{target} ({len(pings)} successful pings)') # type: ignore
    plt.title("Ping Response Times to Multiple Targets") # type: ignore
    plt.xlabel("Time (s)") # type: ignore
    plt.ylabel("Response Time (ms)") # type: ignore
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"ping_results_{timestamp}.png"
    plt.savefig(filename) # type: ignore
    plt.show() # type: ignore

def main():
    parser = argparse.ArgumentParser(description="Ping multiple targets and plot the results.")
    parser.add_argument("--targets", nargs="+", default=["google.com", "xboxlive.com", "msn.com", "1.1.1.1", "8.8.8.8"], help="A list of hosts to ping. Space-separated.")
    parser.add_argument("--pings", type=int, default=3, help="Number of ping attempts per interval.")
    parser.add_argument("--interval", type=int, default=60, help="Interval between ping cycles in seconds.")
    parser.add_argument("--duration", type=int, default=10, help="Duration of the ping test in minutes.")
    args: argparse.Namespace = parser.parse_args()
    default_gateway = get_default_gateway()
    targets: list[str] = args.targets if default_gateway in args.targets or default_gateway == '127.0.0.1' else [*args.targets, default_gateway]
    ping_targets(targets, args.pings, args.interval, args.duration)


if __name__ == "__main__":
    main()