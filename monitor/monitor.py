import redis
import time

def main():
    r = redis.Redis(host='redis', port=6379, db=0)
    while True:
        r.publish('events', 'Ping')
        time.sleep(1)

if __name__ == '__main__':
    main()
