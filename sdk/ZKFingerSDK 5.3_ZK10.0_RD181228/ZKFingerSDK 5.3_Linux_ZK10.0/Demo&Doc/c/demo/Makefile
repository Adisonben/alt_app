CC := gcc
OBJ := main.o
main: $(OBJ)
	$(CC) -o $@ $^ -lpthread -ldl
$(OBJ): main.c
	$(CC) -c $< -o $@
clean:
	rm -f $(OBJ) main

