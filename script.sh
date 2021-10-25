# python3 main.py 3 3 MINIMAX RAND

# echo Inicio dos testes 
# echo 
# for depth in 3 4
# do
# 	echo 
# 	for list_size in 3 4 5
# 	do
# 		echo REGRA: depth: $depth  List_size: $list_size  MINIMAX joga primeiro 
# 		for minimax_first in {1..15..1}
# 		do
# 			echo
# 			echo Execucao num $minimax_first
# 			echo 
# 			python3 main.py $depth $list_size MINIMAX RAND 
# 			echo
# 			echo -------------------
# 		done

# 		echo 

# 		echo depth: $depth  List_size: $list_size  RAND joga primeiro
# 		for rand_first in {1..15..1}
# 		do
# 			echo
# 			echo Execucao num $rand_first
# 			python3 main.py $list_size $depth RAND MINIMAX
# 			echo 
# 			echo -------------------
# 		done
# 		echo 
# 	done
# 	echo
# done


# echo Inicio dos testes RAND vs RAND
# echo 
# for list_size_1 in 2 4 6
# do
# 	echo 
# 	for list_size_2 in 2 4 6
# 	do
# 		echo REGRA: List_size_1: $list_size_1  List_size_2: $list_size_2 RAND vs RAND
# 		for rand_vs_rand in {1..15..1}
# 		do
# 			echo
# 			echo Execucao num $rand_vs_rand
# 			echo 
# 			python3 main.py $list_size_1 $list_size_2 RAND RAND 
# 			echo
# 			echo -------------------
# 		done
# 		echo
# 	done
# 	echo
# done


# echo Inicio dos testes MINMAX vs MINMAX
# echo 
# for depth_1 in 2 3 4
# do
# 	echo 
# 	for depth_2 in 2 3 4
# 	do
# 		echo REGRA: depth_1: $depth_1  depth_2: $depth_2 MINIMAX vs MINIMAX
# 			echo		
# 			python3 main.py $depth_1 $depth_2 MINIMAX MINIMAX 
# 			echo
# 			echo -------------------
		
# 	done
# 	echo
# done





# for a in 1 2 3 4 5
# do
# 	echo EXECUCAO NUMERO $a
# 	echo PARALELO...
# 	for i in 126 512 1024 2048
# 	do
# 		for j in 2 4 8
# 		do
# 			echo MATRIZ $i
# 			time ./paralelo_compilado -m $i -t $j
# 		done	
# 		echo ..............................\n
# 	done

# 	echo SEQUENCIAL...
# 	for k in 126 512 1024 2048
# 	do
# 		echo MATRIZ $k
# 		time ./sequencial_compilado -m $k
# 		echo ..............................\n
# 	done
    

# done


