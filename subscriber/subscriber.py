import redis

def main():
    r = redis.Redis(host='redis', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe(['events'])

    print('Suscriptor esperando mensajes...')
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Mensaje recibido: {message['data'].decode('utf-8')}")

if __name__ == '__main__':
    main()
