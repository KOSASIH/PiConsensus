import random
import networkx as nx
import matplotlib.pyplot as plt
from hypothesis import given, strategies as st
from typing import Dict, Any, List, Callable

# === Agent-Based Network Simulator ===

class Node:
    def __init__(self, node_id: int, is_adversary: bool = False):
        self.node_id = node_id
        self.is_adversary = is_adversary
        self.balance = 1000 if not is_adversary else 10000

    def __repr__(self):
        return f"Node({self.node_id}, adversary={self.is_adversary})"

class NetworkSimulator:
    def __init__(self, num_nodes=10, adversaries=2):
        self.G = nx.erdos_renyi_graph(num_nodes, 0.5)
        self.nodes = [Node(i, i < adversaries) for i in range(num_nodes)]
        self.adversaries = [n for n in self.nodes if n.is_adversary]
        self.honest = [n for n in self.nodes if not n.is_adversary]

    def simulate_attack(self, attack_type: str, rounds: int = 5):
        print(f"\n[Sim] Running {attack_type} attack for {rounds} rounds...")
        if attack_type == "double_spend":
            return self._double_spend_attack(rounds)
        elif attack_type == "sybil":
            return self._sybil_attack(rounds)
        elif attack_type == "network_partition":
            return self._network_partition_attack(rounds)
        else:
            print("Unknown attack type.")
            return None

    def _double_spend_attack(self, rounds):
        results = []
        attacker = self.adversaries[0]
        for r in range(rounds):
            victim = random.choice(self.honest)
            print(f"Round {r + 1}: {attacker} attempts double-spend against {victim}")
            # Simulate double-spend by broadcasting conflicting transactions
            tx1 = {"from": attacker.node_id, "to": victim.node_id, "amount": 100, "nonce": r}
            tx2 = {"from": attacker.node_id, "to": random.choice(self.honest).node_id, "amount": 100, "nonce": r}
            confirmed = random.choice([tx1, tx2])
            results.append(confirmed)
            print(f"Confirmed: {confirmed}")
        return results

    def _sybil_attack(self, rounds):
        results = []
        for r in range(rounds):
            sybil_nodes = [Node(1000 + i, True) for i in range(10)]
            print(f"Round {r + 1}: {len(sybil_nodes)} Sybil nodes injected.")
            self.nodes += sybil_nodes
            self.adversaries += sybil_nodes
            # Simulate consensus voting
            votes = [random.choice(["A", "B"]) for _ in self.nodes]
            majority = max(set(votes), key=votes.count)
            print(f"Majority decision: {majority}")
            results.append({"round": r, "majority": majority, "votes": votes.count(majority)})
        return results

    def _network_partition_attack(self, rounds):
        results = []
        for r in range(rounds):
            # Randomly split network into two
            partition = set(random.sample([n.node_id for n in self.nodes], len(self.nodes)//2))
            print(f"Round {r + 1}: Partition {partition}")
            # Simulate partitioned consensus
            decisions = {pid: random.choice(["yes", "no"]) for pid in partition}
            print(f"Partitioned decisions: {decisions}")
            results.append(decisions)
        return results

    def visualize(self):
        nx.draw(self.G, with_labels=True)
        plt.title("PiConsensus Network Topology")
        plt.show()

# === Fuzzing & Property-Based Testing ===

@given(amount=st.integers(min_value=-10000, max_value=10000))
def test_transaction_validity(amount):
    """Fuzz test: Transaction amounts should be positive and not overflow."""
    assert amount >= 0, "Negative transaction detected!"
    assert amount < 1e9, "Overflow transaction detected!"

# === Example Usage ===

def run_all_simulations():
    net = NetworkSimulator(num_nodes=12, adversaries=3)
    net.visualize()
    print("Double-Spend Attack Results:", net.simulate_attack("double_spend"))
    print("Sybil Attack Results:", net.simulate_attack("sybil"))
    print("Network Partition Attack Results:", net.simulate_attack("network_partition"))
    print("Running transaction fuzz test (property-based)...")
    try:
        test_transaction_validity()
        print("Fuzz tests passed.")
    except AssertionError as e:
        print("Fuzz test failed:", e)

if __name__ == "__main__":
    print("PiConsensus Simulation & Adversarial Test Suite")
    run_all_simulations()
