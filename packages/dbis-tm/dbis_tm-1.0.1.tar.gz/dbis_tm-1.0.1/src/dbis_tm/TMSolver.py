"""
Created 2022-05
Moved here 2023-02

@author: Lara
@author: Marc
@author: Wolfgang
"""
from __future__ import annotations

import itertools
import sys
from dbis_tm import Schedule, OperationType
from typing import Union
from graphviz import Digraph


class Serializability:
    """
    I am an interface for checking the serializability of a given schedule (see Schedule class).
    You should not construct me because I am a stateless interface that merely provides static functions.

    Functions:
        conflict_graph_contains_cycle (helper method)
        remove_aborted_tx (helper method)
        is_serializable (checks membership of CSR class)
        build_graphviz_object
    """

    def __init__(self):
        raise TypeError("Cannot create 'Serializability' instances.")

    @classmethod
    def conflict_graph_contains_cycle(
        cls, graph: dict, current: set[int], start: int, visited: set[int]
    ) -> bool:
        """
        Helper method.
        Uses a simple DFS to detect a cycle in `graph`.

        Returns:
            true iff `start` is part of a cycle.
        """
        for dependency in graph[current]:
            if dependency == start:
                return True
            elif dependency not in visited:
                visited.add(dependency)
                has_cycle = cls.conflict_graph_contains_cycle(
                    graph, dependency, start, visited
                )
                if has_cycle:
                    return True
        return False

    @classmethod
    def remove_aborted_tx(cls, schedule: Union[Schedule, str]) -> None:
        """
        Remove aborted transactions in ``schedule`.

        NOTE: This function operates on the passed object!
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        schedule.operations = list(
            filter(lambda op: op.tx_number not in schedule.aborts, schedule.operations)
        )

    @classmethod
    def is_serializable(cls, schedule: Union[Schedule, str]) -> tuple[bool, dict]:
        """
        Check whether `schedule` is serializable, i.e., whether it's conflict graph contains a cycle.

        Returns:
            true iff schedule is serializable
            conflict graph as adjacency-list
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        # graph[1] = {2,3} means that tx 1 is "in conflict" with txs 2 and 3
        graph = {operation.tx_number: set() for operation in schedule.operations}

        # For each operation i in `operation_list` check all operations i + 1 until n
        # for conflicts (i.e., same resource, not same tx, but one of the operations is a write operation)
        for op1, i in zip(schedule.operations, range(len(schedule.operations))):
            for op2 in schedule.operations[i + 1 :]:
                if op1.resource != op2.resource or op1.tx_number == op2.tx_number:
                    continue
                elif (
                    op1.op_type == OperationType.WRITE
                    or op2.op_type == OperationType.WRITE
                ):
                    graph[op1.tx_number].add(op2.tx_number)

        # Check for each tx whether it is part of a cycle in the conflict graph
        graph_has_cycle = any(
            map(lambda n: cls.conflict_graph_contains_cycle(graph, n, n, set()), graph)
        )
        return not graph_has_cycle, graph

    @classmethod
    def build_graphviz_object(cls, graph: dict) -> Digraph:
        """
        Construct Graphviz directed graph from given adjacency list 'graph'.

        Returns:
            Graphviz Digraph object
        """
        dg = Digraph("")
        for t1 in graph:
            for t2 in graph:
                dg.edge(f"t{t1}", f"t{t2}")
        return dg


class Recovery:
    """
    I am an interface for checking the recoverability of a given schedule (see Schedule class).
    You should not construct me because I am a stateless interface that merely provides static functions.

    Functions:
        reads_from (helper method)
        is_recoverable (checks membership of RC class)
        avoids_cascading_aborts (checks membership of ACA class)
        is_strict (checks membership of ST class)
    """

    def __init__(self):
        raise TypeError("Cannot create 'Recovery' instances.")

    @classmethod
    def reads_from(
        cls, schedule: Union[Schedule, str], tx1: int, resource: str, tx2: int
    ) -> tuple[bool, int]:
        """
        Helper method that implements the "reads from" relation:
        We say that any transaction t_i reads any resource x from any transaction t_j if:
            - w_j(x) <_s r_i(x)
            - not (a_j <_s r_i(x))
            - w_j(x) <_s w_k(x) <_s r_i(x) => a_k <_s r_i(x)
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        for op1, i in zip(schedule.operations, range(len(schedule.operations))):
            if not (
                op1.op_type == OperationType.READ
                and op1.tx_number == tx1
                and op1.resource == resource
            ):
                continue
            elif schedule.aborts.get(tx2, sys.maxsize) < op1.index:
                # possible that the same action is done twice in one schedule, have to check both
                return False, op1.index
            for op2 in reversed(schedule.operations[0:i]):
                if op2.op_type == OperationType.WRITE and op2.resource == op1.resource:
                    if schedule.aborts.get(op2.tx_number, sys.maxsize) < op1.index:
                        continue
                    else:
                        # possible that the same action is done twice in one schedule, have to check both
                        if op2.tx_number == tx2:
                            return True, op1.index
                        else:
                            break
        return False, op1.index

    @classmethod
    def is_recoverable(
        cls, schedule: Union[Schedule, str]
    ) -> tuple[bool, set[tuple[int, str, int, bool]]]:
        """
        Check whether `schedule` s is recoverable, i.e., whether the following holds
        for all transaction pairs t_i, t_j with i != j:
            (t_i reads from t_j in s && c_i is in s) => c_j <_s c_i

        Returns:
            true iff schedule is recoverable
            proof if schedule is recoverable
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        tx_indices = range(1, schedule.tx_count + 1)

        # A counterexample or proof will contain tuples of the form (t_i, resource, t_j, does t_i read from t_j?).
        # Note that the only way to violate RC is that t_i reads from t_j and t_i commits,
        # BUT t_j commits AFTER t_i or t_j is still ACTIVE (i.e., hasn't committed or aborted yet).
        # Hence, in case of a counterexample we know that c_j <_s c_i
        # DOES NOT hold (t_j has not committed yet or is still active)
        proof = set()
        cex = set()
        for i, r, j in itertools.product(tx_indices, schedule.resources, tx_indices):
            if i == j:
                continue
            reads = cls.reads_from(schedule, i, r, j)[0]
            # Equivalent to ("t_i reads r from t_j" AND "c_i in s") IMPLIES "c_j <_s c_i"
            if not (reads and i in schedule.commits) or (
                schedule.commits.get(j, sys.maxsize) < schedule.commits[i]
            ):
                proof.add((i, r, j, reads))
            else:
                cex.add((i, r, j, reads))
        return (False, cex) if len(cex) != 0 else (True, proof)

    @classmethod
    def avoids_cascading_aborts(
        cls, schedule: Union[Schedule, str]
    ) -> tuple[bool, set[tuple[int, str, int, bool]]]:
        """
        Check whether `schedule` s avoids cascading aborts, i.e., whether the following holds
        for all transaction pairs t_i, t_j with i != j:
            t_i reads from t_j in s => c_j <_s r_i(x)

        Returns:
            true iff schedule avoids cascading aborts
            proof if schedule avoids cascading aborts
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        tx_indices = range(1, schedule.tx_count + 1)

        # A counterexample or proof will contain tuples of the form (t_i, resource, t_j, does t_i read from t_j?)
        proof = set()
        cex = set()
        for i, r, j in itertools.product(tx_indices, schedule.resources, tx_indices):
            if i == j:
                continue
            reads, index = cls.reads_from(schedule, i, r, j)
            if reads:
                for op in schedule.operations:
                    if (
                        op.op_type == OperationType.READ
                        and op.tx_number == i
                        and op.resource == r
                        and op.index == index
                        and schedule.commits.get(j, sys.maxsize) >= op.index
                    ):
                        cex.add((i, r, j, reads))
            proof.add((i, r, j, reads))
        return (False, cex) if len(cex) != 0 else (True, proof)

    @classmethod
    def is_strict(
        cls, schedule: Union[Schedule, str]
    ) -> tuple[bool, set[tuple[str, str, bool, bool]]]:
        """
        Check whether `schedule` s is strict, i.e., whether the following holds
        for all transactions t_j and all operations p_i from t_j:
            (w_j(x) <_s p_i(x) && i != j) => (a_j <_s p_i(x) || c_j <_s p_i(x))

        Returns:
            true iff schedule is strict
            proof if schedule is strict
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        # A counterexample or proof will contain tuples of the form (w_j(x), p_i(x), a_j <_s p_i(x), c_j <_s p_i(x))
        proof = set()
        cex = set()
        for op1, i in zip(schedule.operations, range(len(schedule.operations))):
            for op2 in reversed(schedule.operations[0:i]):
                if op1.tx_number == op2.tx_number or op1.resource != op2.resource:
                    continue
                elif op2.op_type == OperationType.WRITE:
                    aborted = (
                        schedule.aborts.get(op2.tx_number, sys.maxsize) < op1.index
                    )
                    committed = (
                        schedule.commits.get(op2.tx_number, sys.maxsize) < op1.index
                    )
                    if not (aborted or committed):
                        cex.add((str(op2), str(op1), aborted, committed))
                    else:
                        proof.add((str(op2), str(op1), aborted, committed))
        return (False, cex) if len(cex) != 0 else (True, proof)


class Scheduling:
    """
    I am an interface for checking the whether a schedule (see Schedule class) can be created by a specific scheduler.
    You should not construct me because I am a stateless interface that merely provides static functions.

    Functions:
        is_2PL (checks whether schedule satisfies 2-phase-locking)
        is_C2PL (checks whether schedule satisfies conservative 2-phase-locking)
        is_S2PL (checks whether schedule satisfies strict 2-phase-locking)
        is_SS2PL (checks whether schedule satisfies strong strict 2-phase-locking)
        is_operations_same (Checks whether the two  given schedules do have the same operations.)
    """

    def __init__(self):
        raise TypeError("Cannot create 'Scheduling' instances.")

    @classmethod
    def is_2PL(cls, schedule: Union[Schedule, str]) -> tuple[bool, list[str]]:
        """
         Check whether `schedule` s satisfies 2-phase-locking, i.e., whether the following holds:
            In the first phase locks can only be set.
            In the second phase locks can only be released. Only possible after all locks have been set.
            All locks have to be removed

        Returns:
            true iff schedule satisfies 2-phase-locking
            empty list if schedule satisfies 2-phase-locking
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]
        errors = []
        transactions = [[]]  # [[1,2,3,...][#1 ][#2][#3]...]
        locks = []  # all things which have to be locked [[locks of transaction 1][...]]
        locks_compatibility = []
        # sort by transaction
        for i in schedule.operations:
            # check for compatibility if locked at the same time
            if (
                i.op_type == OperationType.READ_LOCK
                or i.op_type == OperationType.WRITE_LOCK
            ):
                # check  wether differnt trans, but same resource
                conflict = [
                    t
                    for t in locks_compatibility
                    if t.tx_number != i.tx_number and t.resource == i.resource
                ]
                # check wether both write
                if [t for t in conflict if t.op_type == OperationType.WRITE_LOCK]:
                    errors.append(
                        f"L4: Schreibsperre inkompatibel mit allen andeden Sperren {i, conflict}"
                    )
                elif conflict and i.op_type == OperationType.WRITE_LOCK:
                    errors.append(
                        f"L4: Schreibsperre inkompatibel mit Lesesperren {i, conflict}"
                    )
                else:
                    locks_compatibility.append(i)
            elif (
                i.op_type == OperationType.READ_UNLOCK
                or i.op_type == OperationType.WRITE_UNLOCK
            ):
                locks_compatibility = [
                    op
                    for op in locks_compatibility
                    if i.tx_number != op.tx_number
                    or i.resource != op.resource
                    or (op.op_type.value != "rl" and i.op_type.value == "ru")
                    or (op.op_type.value != "wl" and i.op_type.value == "wu")
                ]

            if i.tx_number not in transactions[0]:
                transactions[0].extend([i.tx_number])
                transactions.append([i])
                locks.append([])
                if (
                    i.op_type == OperationType.READ_LOCK
                    or i.op_type == OperationType.WRITE_LOCK
                ):
                    locks[len(transactions) - 2].extend(
                        [i.op_type.value[0] + str(i.tx_number) + i.resource]
                    )
                    # op_type, tx_number, resource, index)
                    # r, 1, x, an wie vielter stelle
            else:
                index = transactions[0].index(i.tx_number)
                transactions[index + 1].extend([i])
                if (
                    i.op_type == OperationType.READ_LOCK
                    or i.op_type == OperationType.WRITE_LOCK
                ):
                    locks[index].extend(
                        [i.op_type.value[0] + str(i.tx_number) + i.resource]
                    )
        # go through transactions and verify whether they are 2PL
        missed_locks = []
        for i in range(len(transactions[0])):
            locks_set = []
            all_locked = False
            for j in transactions[i + 1]:
                current_op = j.op_type
                representation = j.op_type.value[0] + str(j.tx_number) + j.resource

                if locks_set == locks[i]:  # all locks set?
                    all_locked = True

                if (
                    current_op == OperationType.WRITE_LOCK
                    or current_op == OperationType.READ_LOCK
                ):
                    if representation not in locks_set:
                        locks_set.append(representation)
                        missed_locks.append(representation)
                    else:
                        errors.append(f"L1/L2: Doppelte Sperre: {j}")
                elif (
                    current_op == OperationType.WRITE
                    or current_op == OperationType.READ
                ):
                    if representation not in locks_set:
                        errors.append(f"L2: Nicht gesperrt vor Ausführung: {j}")
                elif (
                    current_op == OperationType.WRITE_UNLOCK
                    or current_op == OperationType.READ_UNLOCK
                ):
                    if all_locked:  # all locked?
                        if representation in locks_set:  # already locked?
                            locks_set.remove(representation)
                            missed_locks.remove(representation)
                        else:
                            errors.append(f"L3: Nicht gesperrt vor entsperren: {j}")
                    else:
                        errors.append(
                            f"2PL: Entsperren bevor alle anderen Sperren gesetzt sind: {j}"
                        )
                        missed_locks.remove(representation)
        if missed_locks:
            errors.append(f"L1: Nicht alle Sperren aufgehoben: {missed_locks}")
        is2PL = not errors
        return is2PL, errors

    @classmethod
    def is_C2PL(cls, schedule: Union[Schedule, str]) -> tuple[bool, list[str]]:
        """
        Check whether `schedule` s satisfies conservative 2-phase-locking, i.e., whether the following holds:
            satisfies 2-phase-locking && all locks of a transaction are set before its first operation

        Returns:
            true iff schedule satisfies conservative 2-phase-locking
            empty list if schedule satisfies conservative 2-phase-locking
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]
        res = cls.is_2PL(schedule)
        if not res[0]:
            return False, res[1]
        locks = []
        for i in range(1, schedule.tx_count + 1):
            tx_ops = list(filter(lambda op: op.tx_number == i, schedule.operations))
            index_last_lock = next(
                (
                    tx_ops.index(op)
                    for op in reversed(tx_ops)
                    if op.op_type in [OperationType.READ_LOCK, OperationType.WRITE_LOCK]
                ),
                sys.maxsize,
            )
            index_first_op = next(
                (
                    tx_ops.index(op)
                    for op in tx_ops
                    if op.op_type in [OperationType.WRITE, OperationType.READ]
                ),
                -sys.maxsize,
            )
            if index_last_lock >= index_first_op:
                locks += [
                    op
                    for op in tx_ops
                    if op.op_type in [OperationType.READ_LOCK, OperationType.WRITE_LOCK]
                    and tx_ops.index(op) > index_first_op
                ]
        if locks:
            return False, [
                f"C2PL: Sperren {locks} wurden nach der ersten r/w Operation gesetzt"
            ]
        return True, []

    @classmethod
    def is_S2PL(cls, schedule: Union[Schedule, str]) -> tuple[bool, list[str]]:
        """
        Check whether `schedule` s satisfies strict 2-phase-locking, i.e., whether the following holds:
            satisfies 2-phase-locking && all write locks of a transaction are held until its last operation

        Returns:
            true iff schedule satisfies strict 2-phase-locking
            empty list if schedule satisfies strict 2-phase-locking
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        res = cls.is_2PL(schedule)
        if not res[0]:
            return False, res[1]
        early_unlocks = []
        late_unlocks = []
        errors = []
        for i in range(1, schedule.tx_count + 1):
            tx_ops = list(filter(lambda op: op.tx_number == i, schedule.operations))
            tx_w_unlocks = list(
                filter(lambda op: op.op_type == OperationType.WRITE_UNLOCK, tx_ops)
            )
            index_first_unlock = next(
                (op.index for op in tx_ops if op.op_type == OperationType.WRITE_UNLOCK),
                sys.maxsize,
            )
            index_last_op = next(
                (
                    op.index
                    for op in reversed(tx_ops)
                    if op.op_type in [OperationType.WRITE, OperationType.READ]
                ),
                -sys.maxsize,
            )
            if index_first_unlock <= index_last_op:
                early_unlocks += [op for op in tx_w_unlocks if op.index < index_last_op]
            final_unlocks = [t for t in tx_ops if t.index > index_last_op]
            if final_unlocks[0].index != index_last_op + 1:
                late_unlocks += [i]
            # have to check wether
            # unlocks after locking all immediately performed
            elif len(final_unlocks) + index_last_op != final_unlocks[-1].index:
                late_unlocks += [i]
        if early_unlocks:
            errors += [
                f"S2PL: {early_unlocks} wurden vor der letzten r/w Operation entsperrt"
            ]
        if late_unlocks:
            errors += [
                f"S2PL: Entsperren von {late_unlocks} ist nicht direkt nach der letzten r/w Operation erfolgt"
            ]
        if errors:
            return False, errors
        return True, []

    @classmethod
    def is_SS2PL(cls, schedule: Union[Schedule, str]) -> tuple[bool, list[str]]:
        """
        Check whether `schedule` s satisfies strong strict 2-phase-locking, i.e., whether the following holds:
            satisfies 2-phase-locking && all read/write locks of a transaction are held until its last operation

        Returns:
            true iff schedule satisfies strong strict 2-phase-locking
            empty list if schedule satisfies strong strict 2-phase-locking
                  else counterexample
        """
        if isinstance(schedule, str):
            schedule = Schedule.parse_schedule(schedule)
            assert not schedule[1]
            schedule = schedule[0]

        res = cls.is_2PL(schedule)
        if not res[0]:
            return False, res[1]

        errors = []
        late_unlocks = []
        early_unlocks = []
        for i in range(1, schedule.tx_count + 1):
            tx_ops = list(filter(lambda op: op.tx_number == i, schedule.operations))
            tx_unlocks = list(
                filter(
                    lambda op: op.tx_number == i
                    and op.op_type
                    in [OperationType.READ_UNLOCK, OperationType.WRITE_UNLOCK],
                    schedule.operations,
                )
            )
            index_first_unlock = next(
                (
                    op.index
                    for op in tx_ops
                    if op.op_type
                    in [OperationType.READ_UNLOCK, OperationType.WRITE_UNLOCK]
                ),
                sys.maxsize,
            )
            index_last_op = next(
                (
                    op.index
                    for op in reversed(tx_ops)
                    if op.op_type in [OperationType.WRITE, OperationType.READ]
                ),
                -sys.maxsize,
            )
            if index_first_unlock <= index_last_op:
                early_unlocks += [op for op in tx_unlocks if op.index < index_last_op]
            if (
                index_last_op
                + len([op for op in tx_unlocks if op.index > index_last_op])
                != tx_unlocks[-1].index
            ):
                late_unlocks.append(i)
        if late_unlocks:
            errors.append(
                f"SS2PL: Entsperren von {late_unlocks} ist nicht direkt nach der letzten r/w Operation erfolgt"
            )
        if early_unlocks:
            errors.append(
                f"SS2PL: {early_unlocks} wurde vor der letzten r/w Operation entsperrt"
            )
        if errors:
            return False, errors
        return True, []
