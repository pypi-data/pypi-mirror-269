import asyncio
import websockets

import json


async def handle_client(websocket, path):
    try:
        # Receive message from client
        message = await websocket.recv()
        data = json.loads(message)  # Parse JSON data

        # Process the dict with 'prompt' and 'conversation'
        prompt = data.get('prompt')
        conversation = data.get('conversation')  # This should be a list of dicts

        # Here you would process the input and generate tokens (mocked as a response)
        response_data = {
            'tokens': ['token1', 'token2', 'token3']  # Replace with actual token generation logic
        }

        # Send the response back to the client
        response = json.dumps(response_data)
        await websocket.send(response)
    except websockets.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # Start the server
    start_server = websockets.serve(handle_client, "localhost", 6789)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
