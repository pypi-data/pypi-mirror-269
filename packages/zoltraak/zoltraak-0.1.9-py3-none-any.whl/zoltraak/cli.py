import argparse
import os
from zoltraak.converter import convert_md_to_py
import zoltraak.llms.claude as claude

def main():
    parser = argparse.ArgumentParser(description="MarkdownファイルをPythonファイルに変換します")
    parser.add_argument("input", help="変換対象のMarkdownファイルのパスまたはテキスト", nargs='?')
    parser.add_argument("--output-dir", help="生成されたPythonファイルの出力ディレクトリ", default="generated")
    parser.add_argument("-p", "--prompt", help="追加のプロンプト情報", default=None)
    parser.add_argument("-c", "--compiler", help="コンパイラー（要件定義書のテンプレート）", default="dev_obj")
    # parser.add_argument("-i", "--interpreter", help="インタプリタータイプ定義書ののパス", default="general_def") TODO

    parser.add_argument("-f", "--formatter", help="コードフォーマッター", default="md_comment")
    args = parser.parse_args()

    if args.input is None:
        print("エラー: 入力ファイルまたはテキストが指定されていません。")
        print("使用方法: zoltraak <mdファイルのパス または テキスト> [オプション]")
        print("例1: zoltraak calc.md -p \"計算機を作りたい\" -c lisp")  # 変更: -c オプションの値から.mdを削除
        print("例2: zoltraak \"本書きたい\"  -c lisp")  # 変更: -c オプションの値から.mdを削除
        return

    if args.input.endswith(".md") or \
       os.path.isfile(args.input) or \
       os.path.isdir(args.input):                                          # 入力がマークダウンファイル、ファイルパス、またはディレクトリパスかどうかを判定
        print(args.input)
        md_file_path = os.path.join("requirements", os.path.basename(args.input))  # - 入力されたMarkdownファイルをrequirements/ディレクトリ内のパスに変更
        output_dir = os.path.abspath(args.output_dir)                      # - 出力ディレクトリの絶対パスを取得
        prompt = args.prompt                                               # - 追加のプロンプト情報を取得
        print("momom")
        print("prompt:", prompt)
        compiler_path = os.path.join("zoltraak/setting/compiler", args.compiler + ".md")    # 変更: コンパイラーのパスに.mdを追加
        formatter_path = os.path.join("zoltraak/setting/formatter", args.formatter + ".md")  # - フォーマッターのパスを設定

        print("compiler_path:", compiler_path)
        print("formatter_path:", formatter_path)

        md_file_rel_path = os.path.relpath(md_file_path, os.getcwd())      # - 現在のディレクトリからのMarkdownファイルの相対パスを取得
        py_file_rel_path = os.path.splitext(md_file_rel_path)[0] + ".py"   # - Markdownファイルの拡張子を.pyに変更して、Pythonファイルの相対パスを作成
        py_file_path = os.path.join(output_dir, py_file_rel_path)          # - 出力ディレクトリとPythonファイルの相対パスを結合して、Pythonファイルの絶対パスを作成

        os.makedirs(os.path.dirname(py_file_path), exist_ok=True)          # - Pythonファイルの出力ディレクトリを再帰的に作成（既に存在する場合は何もしない）
        convert_md_to_py(
            md_file_path,
            py_file_path,
            prompt,
            compiler_path,
            formatter_path,
        )                                                                  # - MarkdownファイルをPythonファイルに変換する関数を呼び出す
    else:                                                                   # 入力がテキストの場合
        text = args.input                                                   # - 入力されたテキストを取得
        
        # claude.pyのgenerate_response関数を利用してmd_file_pathの名前をpromptから考える関数を作成
        def generate_md_file_name(prompt):
            # promptからファイル名を生成するためにgenerate_response関数を利用

            # requirementsディレクトリが存在しない場合は作成する
            requirements_dir = "requirements"
            if not os.path.exists(requirements_dir):
                os.makedirs(requirements_dir)

            # zoltraak/requirements/内のファイル名を全て取得
            existing_files = [file for file in os.listdir(requirements_dir) if file.startswith("def_")]

            print("existing_files:", existing_files)

            # 既存のファイル名と被らないようにファイル名を生成するプロンプトを作成
            file_name_prompt = f"{prompt}に基づいて、要件定義書のファイル名をdef_hogehoge.mdの形式で提案してください。\n"
            file_name_prompt += f"ただし、以下の既存のファイル名と被らないようにしてください。\n{', '.join(existing_files)}\n"
            file_name_prompt += "ファイル名のみをアウトプットしてください。\n"
            # print("file_name_prompt:", file_name_prompt)
            response = claude.generate_response(file_name_prompt)
            file_name = response.strip()
            return f"{file_name}"

        md_file_path = generate_md_file_name(text)  # promptからファイル名を生成
        print(f"新しい要件定義書 '{md_file_path}' が生成されました。")
        prompt = f"{text}"
        # # print(prompt)
        os.system(f"zoltraak {md_file_path} -p \"{prompt}\" -c {args.compiler} -f {args.formatter}")

