from classes import Table, Ball

t = Table(40)
t.ball = Ball((-2, t.size//2), (-1, 0))

rows = ["".join(row) for row in t.draw_paddle(t.draw_ball(t.table_matrix))]

screen = "\n".join(rows)

print(screen)