import { NextResponse } from "next/server"

// Fallback game state for when Python backend is not available
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
  // For now, always use fallback mode to avoid connection issues
  console.log("Using fallback mode (client-side game logic)")
  return NextResponse.json({
    ...createFallbackGameState(),
    info: "Running in browser mode - no backend required!",
  })
}
