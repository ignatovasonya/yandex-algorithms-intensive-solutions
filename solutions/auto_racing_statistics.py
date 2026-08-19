import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
        
    idx = 0
    N = int(data[idx]); idx += 1
    L = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    
    models = []
    for i in range(N):
        x = float(data[idx]); idx += 1
        y = float(data[idx]); idx += 1
        vx = float(data[idx]); idx += 1
        vy = float(data[idx]); idx += 1
        models.append((x, y, vx, vy, i + 1))
    
    collisions = []
    for i in range(N):
        for j in range(i + 1, N):
            x1, y1, vx1, vy1, num1 = models[i]
            x2, y2, vx2, vy2, num2 = models[j]
            
            dx = x2 - x1
            dy = y2 - y1
            dvx = vx1 - vx2
            dvy = vy1 - vy2
            
            if abs(dvx) < 1e-12 and abs(dvy) < 1e-12:
                if abs(dx) < 1e-12 and abs(dy) < 1e-12:
                    collisions.append((0, i, j))
                continue
            
            if abs(dvx) < 1e-12:
                if abs(dx) > 1e-12:
                    continue
                t = dy / dvy
            elif abs(dvy) < 1e-12:
                if abs(dy) > 1e-12:
                    continue
                t = dx / dvx
            else:
                t1 = dx / dvx
                t2 = dy / dvy
                if abs(t1 - t2) > 1e-12:
                    continue
                t = t1
            
            if t >= 0:
                collisions.append((t, i, j))
    
    collisions.sort()
    
    elimination_time = [float('inf')] * N
    
    for i in range(N):
        x, y, vx, vy, num = models[i]
        
        if vx > 0:
            t_finish = (L - x) / vx
        else:
            t_finish = float('inf')
        
        if vy > 0:
            t_top = (W - y) / vy
            if t_top >= 0:
                elimination_time[i] = min(elimination_time[i], t_top)
        elif vy < 0:
            t_bottom = -y / vy
            if t_bottom >= 0:
                elimination_time[i] = min(elimination_time[i], t_bottom)
        
        if vx <= 0:
            elimination_time[i] = 0
    
    active = [True] * N
    for t, i, j in collisions:
        if not active[i] or not active[j]:
            continue
        
        elimination_time[i] = min(elimination_time[i], t)
        elimination_time[j] = min(elimination_time[j], t)
        active[i] = False
        active[j] = False
    
    finish_times = []
    for i in range(N):
        x, y, vx, vy, num = models[i]
        if vx > 0:
            t_finish = (L - x) / vx
            if elimination_time[i] >= t_finish:
                finish_times.append((t_finish, num))
    
    if not finish_times:
        print(0)
        return
    
    min_time = min(t for t, num in finish_times)
    winners = [num for t, num in finish_times if abs(t - min_time) < 1e-12]
    winners.sort()
    
    print(len(winners))
    print(' '.join(map(str, winners)))

if __name__ == "__main__":
    main()
