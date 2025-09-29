import { type NextRequest, NextResponse } from "next/server"

// Simple AI logic for fallback mode
const makeAIMove = (board: string[][]) => {
  const emptyCells: [number, number][] = []
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (board[i][j] === "") {
        emptyCells.push([i, j])
      }
    }
  }

  if (emptyCells.length > 0) {
    return emptyCells[Math.floor(Math.random() * emptyCells.length)]
  }
  return null
}

const checkWin = (board: string[][], player: string): boolean => {
  // Check rows and columns
  for (let i = 0; i < 3; i++) {
    if (
      (board[i][0] === player && board[i][1] === player && board[i][2] === player) ||
      (board[0][i] === player && board[1][i] === player && board[2][i] === player)
    ) {
      return true
    }
  }

  // Check diagonals
  if (
    (board[0][0] === player && board[1][1] === player && board[2][2] === player) ||
    (board[0][2] === player && board[1][1] === player && board[2][0] === player)
  ) {
    return true
  }

  return false
}

const isDraw = (board: string[][]): boolean => {
  return board.every((row) => row.every((cell) => cell !== ""))
}

export async function POST(request: NextRequest) {
  try {
    const { row, col, board } = await request.json()

    if (!board || !Array.isArray(board) || board[row][col] !== "") {
      return NextResponse.json({ error: "Invalid move" }, { status: 400 })
    }

    // Make player move
    const newBoard = board.map((r: string[]) => [...r])
    newBoard[row][col] = "X"

    let status = ""
    let game_over = false

    if (checkWin(newBoard, "X")) {
      status = "🎉 You Win!"
      game_over = true
    } else if (isDraw(newBoard)) {
      status = "🤝 Draw!"
      game_over = true
    } else {
      // Make AI move
      const aiMove = makeAIMove(newBoard)
      if (aiMove) {
        const [aiRow, aiCol] = aiMove
        newBoard[aiRow][aiCol] = "O"

        if (checkWin(newBoard, "O")) {
          status = "😔 AI Wins!"
          game_over = true
        } else if (isDraw(newBoard)) {
          status = "🤝 Draw!"
          game_over = true
        }
      }
    }

    return NextResponse.json({
      board: newBoard,
      player_turn: "X",
      status,
      game_over,
      game_id: "fallback-" + Date.now(),
      fallback_mode: true,
    })
  } catch (error) {
    console.error("Error making move:", error)
    return NextResponse.json({ error: "Failed to make move" }, { status: 500 })
  }
}
