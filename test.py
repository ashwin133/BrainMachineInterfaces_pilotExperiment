import queue

velocity_queue = queue.Queue(maxsize=10)
for _ in range(10):
    velocity_queue.put([0,0])
for i in range(20):
    distanceX, distanceY = velocity_queue.get()
    print(distanceX,distanceY)