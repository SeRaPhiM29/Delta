from pystdf.IO import Parser
from pystdf.Writers import TextWriter  # or some “sink” you want

def main():
    file_path = 'G142621.1_T1_Batch1.stdf'
    text_out_path = 'out.txt'

    with open(file_path, 'rb') as f, open(text_out_path, 'w') as fout:
        parser = Parser(inp=f)
        writer = TextWriter(stream=fout)
        parser.addSink(writer)
        parser.parse()
    print("Parsing done, output at", text_out_path)

if __name__ == '__main__':
    main()
