from term2048.board import Board
from term2048.game import Game

out_file = open("benchmark.txt","w")

for i in range(0,51):
    game = Game()
    score = game.loopIA(sleep_time=0)
    maxVal = game.board.maxValue()
    won = game.board.won()
    out_file.write(str(i)+"\t")
    out_file.write(str(score)+"\t")
    out_file.write(str(maxVal)+"\t")
    out_file.write("\n")
    out_file.flush()
    
