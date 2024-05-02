import os, time

from pypdf import PdfReader, PdfWriter
from term_printer import ColorRGB, cprint
import keyboard

def ReadPdf():

    file_name = input("Input file name: ")

    if os.path.exists(file_name):

        reader = PdfReader(file_name)
        number_of_pages = len(reader.pages)
    
    else:
        print("File Not found")
        return
    
    n = 0 #現在の頁

    read_loop = True
    while read_loop:

        os.system("cls")
        page = reader.pages[n]
        text = page.extract_text()
        cprint(text, attrs=[ColorRGB(100, 100, 100)])
        print(f"{n + 1} / {number_of_pages}")

        while True:

            
            time.sleep(0.1)
            if keyboard.is_pressed('right') and n != number_of_pages-1:
                n += 1
                break
            
            elif keyboard.is_pressed('left') and n != 0:
                n-= 1
                break

            elif keyboard.is_pressed('space'):

                read_loop = False
                break
    
    os.system('cls')

def CombinePdf(input_paths, output_path):

    if len(input_paths) <= 1:
        
        cprint("結合するファイルを２つ以上選択してください", attrs=[ColorRGB(0, 255, 0)])
        return

    for l in input_paths:
        
        cprint(l, attrs=[ColorRGB(255, 0, 0)])

    cprint("以上の順でPDFファイルを結合します。よろしいですか YES(y) NO(other)", attrs=[ColorRGB(255, 0, 0)])

    if input("> ") == "y":
        pass

    else:
        return


    merger = PdfWriter()
    for pdf in input_paths:
        merger.append(pdf)

    if not os.path.exists("./Combined"):
        os.mkdir("./Combined")

    merger.write(output_path)
    merger.close()

def DividPdf():

    pass

def PickPage():

    file_name = input("操作するファイルを入力\n>")

    if not ".pdf" in file_name:
        file_name += ".pdf"

    if not os.path.exists(file_name):
        print("ファイルが存在しません")

    else:
        page = int(input("取り出すページを入力\n>")) - 1

        reader = PdfReader(file_name)
        number_of_pages = len(reader.pages)

        if page >= 1 and page <= number_of_pages:
            
            if not os.path.exists("./Picked"):
                os.mkdir("./Picked")

            picker = reader[page]
            picker.write(f"./Picked/{file_name}_picked_{page+1}.pdf")
            picker.close()

        else:
            print("不正なページが入力されました")

def main():

    os.system('cls')

    combine_list = []

    cprint("WELCOME TO PDF OPERATOR\n THIS MESSAGE APPEARS FIRST LUNCHING TIME", attrs=[ColorRGB(100, 100, 100)])
    while True:

        current_path = os.getcwd()
        command = input(f"(PyDF) {current_path}> ")

        if command == "quit":

            print("終了しますか？ : Yes(y) No(other)")
            yesno = input(">>")

            if yesno == "Y" or yesno == "y":
                
                os.system('cls')
                break
            else:
                pass

        elif command == "help":
            
            print("______________________________________________________\n" \
                  "|HOW TO USE PDF OPERATOR                             |\n" \
                  "|____________________________________________________|\n" \
                  "|COMMAND     |DETAILS                                |\n" \
                  "|------------+---------------------------------------|\n" \
                  "|readpdf     |show text of pdf file                  |\n" \
                  "|combinepdf  |combine pdf files appended list        |\n" \
                  "|appendpdf   |append pdf files wanted to combine     |\n" \
                  "|c-ls        |show list appended pdf files           |\n" \
                  "|dividpdf    |divid pdf files (2 files from 1 file)  |\n" \
                  "|pickpage    |pick the page up from pdf file         |\n" \
                  "|quit        |quit pdf operator                      |\n" \
                  "|____________________________________________________|\n" \
                 )

        elif command == "readpdf":
            ReadPdf()

        elif command == "appendpdf":

            print("結合に追加するファイルを選択")
            append_file = input(">>")
            if os.path.exists(append_file):
                combine_list.append(append_file)

                print(f"{append_file} を結合リストに追加しました")
            else:
                print("ファイルが存在しません")

        elif command == "chorder":

            arrow = 0
            num_file = len(combine_list)
            selected = False
            order_loop = True
            while order_loop:

                os.system("cls")
                n = 0
                for l in combine_list:

                    if n == arrow and not selected:
                        print(f"▶ {l}")
                    elif n == arrow and selected:
                        print(f"▷ {l}")
                    else:
                        print(f"　{l}")
                    
                    n += 1

                while True:

                    time.sleep(0.1)
                    if keyboard.is_pressed("down"):
                    
                        if arrow <= num_file-2 and selected:
                            combine_list[arrow], combine_list[arrow+1] = combine_list[arrow+1], combine_list[arrow]
                            arrow += 1
                            break
                        
                        elif arrow != num_file-1 and not selected:
                            arrow += 1
                            break

                    elif keyboard.is_pressed("up"):
                    
                        if arrow != 0 and selected:
                            combine_list[arrow], combine_list[arrow-1] = combine_list[arrow-1], combine_list[arrow]
                            arrow -= 1
                            break

                        elif keyboard.is_pressed("up") and arrow != 0 and not selected:
                            arrow -= 1
                            break


                    elif keyboard.is_pressed("return"):
                        
                        if selected:
                            selected = False
                            break

                        else:
                            selected = True
                            break

                    if keyboard.is_pressed("space"):
                    
                        order_loop = False
                        os.system("cls")
                        break


                

        elif command == "c-ls":

            if len(combine_list) == 0:
                cprint("Files aren't existed", attrs=[ColorRGB(100, 100, 100)])
                
            for i in combine_list:
                cprint(i, attrs=[ColorRGB(0, 0, 100)])

        elif command == "droppdf":

            drop_file = input("結合リストから除外するファイルを入力：")
            print(f"{drop_file} を結合リストから除外します。よろしいですか：YES(y) NO(other)")
            yesno = input(">")

            if (yesno == "y") | (yesno == "Y"):

                combine_list.remove(drop_file)
                print(f"結合リストから初めの {drop_file} を除外しました")

            else:

                print("キャンセルしました")


        elif command == "combinepdf":

            CombinePdf(combine_list, "./Combined/combined.pdf")

        elif command == "dividpdf":
            DividPdf()

        elif command == "pickpage":
            PickPage()

        else:
            os.system(command)

if __name__ == "__main__":

    main()