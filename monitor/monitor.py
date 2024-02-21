import redis
import time

def main():
    r = redis.Redis(host='redis', port=6379, db=0)
    while True:
        r.publish('events', 'Monitor event')
        time.sleep(10)

if __name__ == '__main__':
    main()
