import gym
import l3c.mazeworld
from l3c.mazeworld import MazeTaskSampler

if __name__=='__main__':
    maze_env = gym.make("mazeworld-continuous-3D-v0", task_type="SURVIVAL", max_steps=5000)
    n = 15
    task = MazeTaskSampler(n=n, cell_size=2.0, wall_height=3.2, allow_loops=True, crowd_ratio=0.35, step_reward=-0.001)
    maze_env.set_task(task)
    while True:
        maze_env.reset()
        done=False
        sum_reward = 0
        while not done:
            maze_env.render()
            state, reward, done, _ = maze_env.step(None)
            sum_reward += reward
        if(not maze_env.key_done):
            print("Episode is over! You got %.1f score."%sum_reward)
            maze_env.save_trajectory("trajectory_%dx%d.png"%(n, n))
            if(sum_reward > 0.0):
                n += 2 # gradually increase the difficulty
                print("Increase the difficulty, n = %d"%n)
            task = MazeTaskSampler(n=n, cell_size=2.0, wall_height=3.2, allow_loops=True, crowd_ratio=0.35, step_reward=-0.001)
            maze_env.set_task(task)
        else:
            break
