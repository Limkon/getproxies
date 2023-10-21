import base64
import sys

def encode_file(file_path, encoded_file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    encoded_content = base64.b64encode(content.encode()).decode()

    with open(encoded_file_path, 'w') as file:
        file.write(encoded_content)

    print('文件内容已经成功进行了Base64编码，并保存到', encoded_file_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('请提供文件名和编码后的文件名作为参数')
        print('示例: python base64_encode.py input.txt encoded.txt')
        sys.exit(1)

    file_path = sys.argv[1]
    encoded_file_path = sys.argv[2]

    encode_file(file_path, encoded_file_path)
