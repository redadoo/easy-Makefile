#!/usr/bin/env python3
import os

def have_header(files):
    for file in files:
        if file.endswith(".h"):
            return True
    return False

def write_makefile(name, compiler, flag, project_path):
    with open('Makefile', 'w') as f:
        f.write(f"NAME = {name}\n\n")

        for root, dirs, files in os.walk(project_path):
            if os.path.basename(root) == "EasyMakefile":
                continue

            if files:
                f.write(f'{os.path.basename(root).upper()} = ')
                f.write(' '.join([os.path.relpath(os.path.join(root, file), project_path) for file in files]) + '\n\n')

        f.write("SRCS = ")
        for root, dirs, files in os.walk(project_path):
            if have_header(files):
                continue
            if os.path.basename(root) == "EasyMakefile":
                continue
            if files:
                f.write(f"$({os.path.basename(root).upper()}) ")

        if flag:
            f.write(f'\nFLAGS = {flag}\n')

        f.write("\n")
        f.write(f'CC = {compiler}\n\n')
        f.write("OBJ = *.o\n\n")
        f.write("RM = rm -rf\n\n")
        f.write("all: $(NAME)\n\n")
        f.write("$(NAME): $(OBJ)\n\t")
        f.write('@echo "     - Compiling $(NAME)..."\n\t')
        f.write('@${CC} $(FLAGS) $(OBJ) -o $(NAME)\n\t')
        f.write('@echo "- Compiled -"\n\t')
        f.write('@${RM} $(OBJ)\n\n')
        f.write("$(OBJ): $(SRCS)\n\t")
        f.write('@echo "     - Making object files..."\n\t')
        f.write('@${CC} -c $(SRCS)\n\n')
        f.write("clean:\n\t")
        f.write('@${RM} ${OBJ}\n\n')
        f.write("fclean:\n\t")
        f.write('@${RM} ${NAME}\n\n')
        f.write("re : fclean all\n\n")
        f.write(".PHONY: clean fclean")
        
def get_all_files(path):
    file_list = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".c") or file.endswith(".h"):
                file_list.append(file)
    return file_list

def main():
    name = input("Name of the executable: ")
    compiler = input("Write the name of the compiler: ")
    flag = input("Write compiler flags (leave blank if none): ")
    project_path = input("Enter the project path (leave blank to use the current directory): ")

    if not project_path:
        project_path = os.getcwd()

    write_makefile(name, compiler, flag, project_path)
    

    
if __name__ == "__main__":
    main()
