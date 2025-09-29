import { NextResponse } from "next/server"

const createFallbackGameState = () => ({
  board: [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""],
  ],
  player_turn: "X",
  status: "",
  game_over: false,
  game_id: "fallback-" + Date.now(),
  fallback_mode: true,
})

export async function POST() {
  // Always use fallback mode for now
  return NextResponse.json({
    ...createFallbackGameState(),
    info: "Game reset - running in browser mode",
  })
}
