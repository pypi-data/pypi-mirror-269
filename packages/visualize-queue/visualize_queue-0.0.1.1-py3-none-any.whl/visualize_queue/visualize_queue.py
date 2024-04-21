import matplotlib.pyplot as plt

class QueueVisualization:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)
        self.visualize()

    def dequeue(self):
        if len(self.queue) == 0:
            print("Queue is empty")
            return None
        item = self.queue.pop(0)
        self.visualize()
        return item

    def visualize(self):
        plt.clf()
        plt.bar(range(len(self.queue)), self.queue, color='black')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Queue Visualization')
        plt.ylim(0, max(self.queue) + 1 if self.queue else 10)  # Set dynamic y-axis limit
        plt.pause(3) # Wait 3 seconds
