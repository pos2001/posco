# each of the circuits has only one 𝑋 rotation gate with a random angle. The circuit is repeated five times with different random rotations

import os
import numpy as np

from braket.aws import AwsDevice
from braket.circuits import Circuit
from braket.jobs import save_job_result
from braket.tracking import Tracker

t = Tracker().start()

print("Test job started!")

# Use the device declared in the creation script
device = AwsDevice(os.environ["AMZN_BRAKET_DEVICE_ARN"])

#측정 결과와 각도 값을 저장할 빈 리스트를 초기화
counts_list = []
angle_list = []

for _ in range(5):
    # 임의의 각도 값을 생성
    angle = np.pi * np.random.randn()
    
    # 임의의 각도로 X 회전 게이트를 적용한 양자 회로를 생성
    random_circuit = Circuit().rx(0, angle)

    task = device.run(random_circuit, shots=100)
    counts = task.result().measurement_counts

    # 각도와 측정 결과를 리스트에 추가
    angle_list.append(angle)
    counts_list.append(counts)
    print(counts)

# Save the variables of interest so that we can access later
# 측정 결과, 각도 값, 그리고 예상 실행 비용을 저장
save_job_result({"counts": counts_list, "angle": angle_list, "estimated cost": t.qpu_tasks_cost() + t.simulator_tasks_cost()})

print("Test job completed!")