all:
	make run_1
	make run_2
	make run_3

run_1:
	python3 compilador.py exemplo1.lcc

run_2:
	python3 compilador.py exemplo2.lcc

run_3:
	python3 compilador.py exemplo3.lcc
