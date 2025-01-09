from collections import defaultdict
import sys, asyncio, ast

topics = defaultdict(lambda: [])

async def handle_client(reader, writer):

    line = str()
    while line.strip() != 'quit':

        line = (await reader.readline()).decode('utf8')

        if line.strip() == '': 
            continue


        cmd = ast.literal_eval(line)

        if cmd['command'] == 'subscribe':
            topics[cmd['topic']].append(writer)
        elif cmd['command'] == 'publish':
            writers = topics[cmd['topic']]
            for w in writers:
                w.write(line.encode('utf8'))
        elif cmd['command'] == 'filter':
            writers = topics[cmd['topic']]
            for w in writers:
                w.write(line.encode('utf8'))

    writer.close()
