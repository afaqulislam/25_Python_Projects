"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import {
  Trophy,
  Zap,
  Brain,
  User,
  Bot,
  RotateCcw,
  Home,
  Settings,
  Volume2,
  VolumeX,
  ArrowLeft,
  Award,
  Target,
  Gamepad2,
  Info,
  Github,
  Linkedin,
  Mail,
  Globe,
  Heart,
  Code,
  Coffee,
  Star,
  Loader2,
  Sparkles,
  Frown,
  Smile,
} from "lucide-react"
import { InitialLoader } from "@/components/initial-loader"
import { ResultPopup } from "@/components/result-popup"

type Player = "X" | "O" | ""
type Board = Player[][]
type Difficulty = "easy" | "medium" | "hard"
type Screen = "menu" | "game" | "settings" | "about"

interface GameState {
  board: Board
  status: string
  player_turn: string
  game_over: boolean
  game_id?: string
  fallback_mode?: boolean
  warning?: string
  info?: string
}

interface GameStats {
  wins: number
  losses: number
  draws: number
  streak: number
  totalGames: number
  bestStreak: number
}

interface GameSettings {
  soundEnabled: boolean
  musicEnabled: boolean
  volume: number
  difficulty: Difficulty
  animations: boolean
}

export default function TicTacToeGame() {
  const [initialLoading, setInitialLoading] = useState(true)
  const [webLoading, setWebLoading] = useState(true)
  const [gameMode, setGameMode] = useState<"ai" | "human" | null>(null)
  const [showResultPopup, setShowResultPopup] = useState(false)
  const [currentPlayer, setCurrentPlayer] = useState<"X" | "O">("X")

  const [gameState, setGameState] = useState<GameState | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [animatingCell, setAnimatingCell] = useState<string | null>(null)
  const [makingMove, setMakingMove] = useState(false)
  const [aiThinking, setAiThinking] = useState(false)
  const [winningCells, setWinningCells] = useState<string[]>([])
  const [currentScreen, setCurrentScreen] = useState<Screen>("menu")
  const [showCelebration, setShowCelebration] = useState(false)
  const [gameResult, setGameResult] = useState<"win" | "lose" | "draw" | null>(null)

  const [gameStats, setGameStats] = useState<GameStats>({
    wins: 0,
    losses: 0,
    draws: 0,
    streak: 0,
    totalGames: 0,
    bestStreak: 0,
  })

  const [settings, setSettings] = useState<GameSettings>({
    soundEnabled: true,
    musicEnabled: true,
    volume: 75,
    difficulty: "medium",
    animations: true,
  })

  // Load saved data on component mount
  useEffect(() => {
    const savedStats = localStorage.getItem("tictactoe-stats")
    if (savedStats) {
      setGameStats(JSON.parse(savedStats))
    }

    const savedSettings = localStorage.getItem("tictactoe-settings")
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings))
    }
  }, [])

  // Web loading effect (on page refresh)
  useEffect(() => {
    const webTimer = setTimeout(() => {
      setWebLoading(false)
    }, 3000) // 3 second web loading animation

    return () => clearTimeout(webTimer)
  }, [])

  // Initial loading effect
  useEffect(() => {
    const timer = setTimeout(() => {
      setInitialLoading(false)
    }, 3000) // 3 second loading animation

    return () => clearTimeout(timer)
  }, [])

  // Save functions
  const saveStats = (newStats: GameStats) => {
    setGameStats(newStats)
    localStorage.setItem("tictactoe-stats", JSON.stringify(newStats))
  }

  const saveSettings = (newSettings: GameSettings) => {
    setSettings(newSettings)
    localStorage.setItem("tictactoe-settings", JSON.stringify(newSettings))
  }

  const updateStats = (result: "win" | "loss" | "draw") => {
    const newStats = { ...gameStats }
    newStats.totalGames += 1

    if (result === "win") {
      newStats.wins += 1
      newStats.streak += 1
      if (newStats.streak > newStats.bestStreak) {
        newStats.bestStreak = newStats.streak
      }
    } else if (result === "loss") {
      newStats.losses += 1
      newStats.streak = 0
    } else {
      newStats.draws += 1
    }

    saveStats(newStats)
  }

  const resetStats = () => {
    const emptyStats = {
      wins: 0,
      losses: 0,
      draws: 0,
      streak: 0,
      totalGames: 0,
      bestStreak: 0,
    }
    saveStats(emptyStats)
  }

  const playSound = (type: "move" | "win" | "lose" | "draw") => {
    if (!settings.soundEnabled) return

    // Simple audio feedback using Web Audio API
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()

    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)

    // Different frequencies for different sounds
    const frequencies = {
      move: 800,
      win: 1200,
      lose: 400,
      draw: 600,
    }

    oscillator.frequency.setValueAtTime(frequencies[type], audioContext.currentTime)
    gainNode.gain.setValueAtTime((settings.volume / 100) * 0.1, audioContext.currentTime)
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3)

    oscillator.start(audioContext.currentTime)
    oscillator.stop(audioContext.currentTime + 0.3)
  }

  const initializeGame = async (mode: "ai" | "human") => {
    setLoading(true)
    setError(null)
    setWinningCells([])
    setShowCelebration(false)
    setGameResult(null)
    setShowResultPopup(false)
    setGameMode(mode)
    setCurrentPlayer("X")

    try {
      const response = await fetch("/api/game/init", {
        method: "POST",
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setGameState(data)
      setCurrentScreen("game")
    } catch (error) {
      console.error("Failed to initialize game:", error)
      setError("Failed to initialize game. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const checkWinningCells = (board: Board, player: Player): string[] => {
    const winPatterns = [
      ["0-0", "0-1", "0-2"],
      ["1-0", "1-1", "1-2"],
      ["2-0", "2-1", "2-2"],
      ["0-0", "1-0", "2-0"],
      ["0-1", "1-1", "2-1"],
      ["0-2", "1-2", "2-2"],
      ["0-0", "1-1", "2-2"],
      ["0-2", "1-1", "2-0"],
    ]

    for (const pattern of winPatterns) {
      const [a, b, c] = pattern
      const [row1, col1] = a.split("-").map(Number)
      const [row2, col2] = b.split("-").map(Number)
      const [row3, col3] = c.split("-").map(Number)

      if (board[row1][col1] === player && board[row2][col2] === player && board[row3][col3] === player) {
        return pattern
      }
    }
    return []
  }

  const makeMove = async (row: number, col: number) => {
    if (!gameState || gameState.board[row][col] !== "" || gameState.game_over || makingMove) return

    setMakingMove(true)
    setAnimatingCell(`${row}-${col}`)
    setError(null)

    playSound("move")

    try {
      if (gameMode === "human") {
        // Human vs Human mode
        const newBoard: Board = gameState.board.map((r) => [...r]) as Board
        newBoard[row][col] = currentPlayer

        let status = ""
        let game_over = false
        let resultType: "win" | "lose" | "draw" | null = null

        if (checkWinningCells(newBoard, currentPlayer).length > 0) {
          status = `🎉 Player ${currentPlayer} Wins!`
          game_over = true
          resultType = "win"
          setWinningCells(checkWinningCells(newBoard, currentPlayer))
          setShowResultPopup(true)
          updateStats("win")
          playSound("win")

          // Auto-hide result animation after 3 seconds
          setTimeout(() => {
            setGameResult(null)
          }, 3000)

          // Auto-hide result popup after 3 seconds
          setTimeout(() => {
            setShowResultPopup(false)
          }, 3000)
        } else if (isDraw(newBoard)) {
          status = "🤝 Draw!"
          game_over = true
          resultType = "draw"
          setShowResultPopup(true)
          updateStats("draw")
          playSound("draw")

          // Auto-hide result animation after 3 seconds
          setTimeout(() => {
            setGameResult(null)
          }, 3000)

          // Auto-hide result popup after 3 seconds
          setTimeout(() => {
            setShowResultPopup(false)
          }, 3000)
        }

        if (resultType) {
          setGameResult(resultType)
        }

        setGameState({
          board: newBoard,
          status,
          game_over,
          player_turn: currentPlayer === "X" ? "O" : "X",
          game_id: "human-" + Date.now(),
        })

        // Switch to next player only if game is not over
        if (!game_over) {
          setCurrentPlayer(currentPlayer === "X" ? "O" : "X")
        }
      } else {
        // AI mode (existing logic)
        setAiThinking(true)

        const requestBody = {
          row,
          col,
          board: gameState.board,
          fallback_mode: true,
          difficulty: settings.difficulty,
        }

        const response = await fetch("/api/game/move", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()

        if (data.error) {
          throw new Error(data.error)
        }

        await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1500))

        setGameState(data)
        setAiThinking(false)

        if (data.game_over) {
          if (data.status.includes("You Win")) {
            const winning = checkWinningCells(data.board, "X")
            setWinningCells(winning)
            setGameResult("win")
            setShowResultPopup(true)
            if (settings.animations) {
              setShowCelebration(true)
              setTimeout(() => setShowCelebration(false), 3000)
            }
            updateStats("win")
            playSound("win")

            // Auto-hide result animation after 3 seconds
            setTimeout(() => {
              setGameResult(null)
            }, 3000)

            // Auto-hide result popup after 3 seconds
            setTimeout(() => {
              setShowResultPopup(false)
            }, 3000)
          } else if (data.status.includes("AI Wins")) {
            const winning = checkWinningCells(data.board, "O")
            setWinningCells(winning)
            setGameResult("lose")
            setShowResultPopup(true)
            updateStats("loss")
            playSound("lose")

            // Auto-hide result animation after 3 seconds
            setTimeout(() => {
              setGameResult(null)
            }, 3000)

            // Auto-hide result popup after 3 seconds
            setTimeout(() => {
              setShowResultPopup(false)
            }, 3000)
          } else if (data.status.includes("Draw")) {
            setGameResult("draw")
            setShowResultPopup(true)
            updateStats("draw")
            playSound("draw")

            // Auto-hide result animation after 3 seconds
            setTimeout(() => {
              setGameResult(null)
            }, 3000)

            // Auto-hide result popup after 3 seconds
            setTimeout(() => {
              setShowResultPopup(false)
            }, 3000)
          }
        }
      }

      setTimeout(() => {
        setAnimatingCell(null)
      }, 300)
    } catch (error) {
      console.error("Failed to make move:", error)
      setError("Failed to make move. Please try again.")
      setAiThinking(false)
    } finally {
      setMakingMove(false)
    }
  }

  const isDraw = (board: string[][]): boolean => {
    return board.every((row) => row.every((cell) => cell !== ""))
  }

  const resetGame = async () => {
    setLoading(true)
    setError(null)
    setWinningCells([])
    setShowCelebration(false)
    setGameResult(null)
    setShowResultPopup(false)
    setAiThinking(false)
    setCurrentPlayer("X")

    try {
      const response = await fetch("/api/game/reset", {
        method: "POST",
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setGameState(data)
      setAnimatingCell(null)
    } catch (error) {
      console.error("Failed to reset game:", error)
      setError("Failed to reset game. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  // Beautiful Web Loader Component (for page refresh)
  // Inside TicTacToeGame component
  const WebLoader = () => {
    // New state to store stable random values for floating icons
    const [floatingIconStyles, setFloatingIconStyles] = useState<
      { left: string; top: string; animationDelay: string; animationDuration: string }[]
    >([]);

    useEffect(() => {
      // Generate random values only once on the client-side
      const styles = [...Array(12)].map(() => ({
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`,
        animationDuration: `${4 + Math.random() * 2}s`,
      }));
      setFloatingIconStyles(styles);
    }, []); // Empty dependency array ensures this runs only once on mount

    return (
      <div className="fixed inset-0 z-[100] bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-72 h-72 bg-indigo-500/20 rounded-full blur-3xl animate-pulse delay-500"></div>
        </div>

        {/* Floating Icons */}
        <div className="absolute inset-0 overflow-hidden">
          {floatingIconStyles.map((style, i) => ( // Use the state variable here
            <div
              key={i}
              className="absolute animate-float opacity-30"
              style={style} // Apply the pre-calculated style
            >
              {i % 4 === 0 && <Trophy className="w-6 h-6 text-yellow-400" />}
              {i % 4 === 1 && <Zap className="w-6 h-6 text-blue-400" />}
              {i % 4 === 2 && <Brain className="w-6 h-6 text-purple-400" />}
              {i % 4 === 3 && <Sparkles className="w-6 h-6 text-pink-400" />}
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className="relative z-10 text-center p-8">
          {/* Logo */}
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full shadow-2xl animate-pulse">
              <Trophy className="w-16 h-16 text-white" />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-6xl font-black text-white mb-4 tracking-tight animate-fade-in">
            TIC TAC TOE{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">PRO</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl text-blue-200 mb-8 animate-fade-in delay-500">Loading Ultimate Gaming Experience...</p>

          {/* Loading Animation */}
          <div className="relative mb-6">
            <div className="w-64 mx-auto">
              <div className="bg-white/20 rounded-full h-2 overflow-hidden">
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-full rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>

          {/* Loading Dots */}
          <div className="flex justify-center space-x-2">
            <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce delay-100"></div>
            <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce delay-200"></div>
          </div>

          {/* Loading Text */}
          <p className="text-white/60 text-sm mt-4 animate-pulse">Preparing your gaming arena...</p>
        </div>

        <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-30px) rotate(180deg); }
        }
        @keyframes fade-in {
          0% { opacity: 0; transform: translateY(20px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-float {
          animation: float 5s ease-in-out infinite;
        }
        .animate-fade-in {
          animation: fade-in 1s ease-out;
        }
        .delay-500 {
          animation-delay: 0.5s;
        }
      `}</style>
      </div>
    );
  };

  // Beautiful Loader Component
  const BeautifulLoader = ({ message }: { message: string }) => (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-lg bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl">
        <CardContent className="p-8 sm:p-12 text-center">
          <div className="relative mb-8">
            {/* Outer spinning ring */}
            <div className="w-20 h-20 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto"></div>
            {/* Inner pulsing ring */}
            <div className="absolute inset-0 w-20 h-20 border-4 border-transparent border-t-blue-400 rounded-full animate-ping mx-auto opacity-20"></div>
            {/* Center icon */}
            <div className="absolute inset-0 flex items-center justify-center">
              <Brain className="w-8 h-8 text-blue-400 animate-pulse" />
            </div>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold text-white mb-2">{message}</h3>
          <p className="text-blue-200 text-sm sm:text-base">AI is warming up on {settings.difficulty} difficulty...</p>
          {/* Loading dots */}
          <div className="flex justify-center space-x-1 mt-4">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-100"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-200"></div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  // Win/Lose/Draw Animation Component
  // const GameResultAnimation = ({ result }: { result: "win" | "lose" | "draw" }) => {
  //   const configs = {
  //     win: {
  //       icon: Sparkles,
  //       title: "🎉 Victory!",
  //       subtitle: "You defeated the AI!",
  //       bgColor: "from-green-500/20 to-emerald-500/20",
  //       borderColor: "border-green-400/30",
  //       iconColor: "text-green-400",
  //       particles: "bg-green-400",
  //     },
  //     lose: {
  //       icon: Frown,
  //       title: "😔 Defeat",
  //       subtitle: "AI wins this round!",
  //       bgColor: "from-red-500/20 to-pink-500/20",
  //       borderColor: "border-red-400/30",
  //       iconColor: "text-red-400",
  //       particles: "bg-red-400",
  //     },
  //     draw: {
  //       icon: Smile,
  //       title: "🤝 Draw!",
  //       subtitle: "Great match!",
  //       bgColor: "from-yellow-500/20 to-orange-500/20",
  //       borderColor: "border-yellow-400/30",
  //       iconColor: "text-yellow-400",
  //       particles: "bg-yellow-400",
  //     },
  //   }

  //   const config = configs[result]
  //   const IconComponent = config.icon

  //   return (
  //     <div className="absolute inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
  //       {/* Backdrop */}
  //       <div className="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

  //       {/* Floating particles */}
  //       {result === "win" &&
  //         [...Array(15)].map((_, i) => (
  //           <div
  //             key={i}
  //             className={`absolute w-2 h-2 ${config.particles} rounded-full animate-bounce opacity-80`}
  //             style={{
  //               left: `${20 + Math.random() * 60}%`,
  //               top: `${20 + Math.random() * 60}%`,
  //               animationDelay: `${Math.random() * 2}s`,
  //               animationDuration: `${1 + Math.random()}s`,
  //             }}
  //           />
  //         ))}

  //       {/* Result card */}
  //       <Card
  //         className={`relative bg-gradient-to-br ${config.bgColor} backdrop-blur-xl ${config.borderColor} border-2 shadow-2xl animate-in zoom-in-50 duration-500`}
  //       >
  //         <CardContent className="p-6 sm:p-8 text-center">
  //           <div className="mb-6">
  //             <IconComponent className={`w-16 h-16 sm:w-20 sm:h-20 ${config.iconColor} mx-auto animate-pulse`} />
  //           </div>
  //           <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">{config.title}</h2>
  //           <p className="text-white/80 text-sm sm:text-base">{config.subtitle}</p>
  //         </CardContent>
  //       </Card>
  //     </div>
  //   )
  // }

  // AI Thinking Component
  const AIThinkingIndicator = () => (
    <div className="flex items-center justify-center gap-2 text-red-300 animate-pulse">
      <Loader2 className="w-4 h-4 animate-spin" />
      <span className="text-xs sm:text-sm">AI is thinking</span>
      <div className="flex space-x-1">
        <div className="w-1 h-1 bg-red-400 rounded-full animate-bounce"></div>
        <div className="w-1 h-1 bg-red-400 rounded-full animate-bounce delay-100"></div>
        <div className="w-1 h-1 bg-red-400 rounded-full animate-bounce delay-200"></div>
      </div>
    </div>
  )

  // Show web loader on page refresh
  if (webLoading) {
    return <WebLoader />
  }

  // Settings Screen
  if (currentScreen === "settings") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        </div>

        <div className="relative z-10 flex flex-col min-h-screen p-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <Button
              variant="outline"
              onClick={() => setCurrentScreen("menu")}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <h1 className="text-xl sm:text-2xl font-bold text-white text-center">Settings</h1>
            <div className="w-20"></div>
          </div>

          <div className="flex-1 flex items-center justify-center">
            <Card className="w-full max-w-md bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl">
              <CardContent className="p-6 sm:p-8 space-y-6 sm:space-y-8">
                {/* Audio Settings */}
                <div className="space-y-4 sm:space-y-6">
                  <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <Volume2 className="w-4 h-4 sm:w-5 sm:h-5" />
                    Audio Settings
                  </h3>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-white text-sm sm:text-base">Sound Effects</span>
                      <Switch
                        checked={settings.soundEnabled}
                        onCheckedChange={(checked) => saveSettings({ ...settings, soundEnabled: checked })}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-white text-sm sm:text-base">Background Music</span>
                      <Switch
                        checked={settings.musicEnabled}
                        onCheckedChange={(checked) => saveSettings({ ...settings, musicEnabled: checked })}
                      />
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-white text-sm sm:text-base">Volume</span>
                        <span className="text-blue-300 text-sm">{settings.volume}%</span>
                      </div>
                      <Slider
                        value={[settings.volume]}
                        onValueChange={(value) => saveSettings({ ...settings, volume: value[0] })}
                        max={100}
                        step={5}
                        className="w-full"
                      />
                    </div>
                  </div>
                </div>

                {/* Game Settings */}
                <div className="space-y-4 sm:space-y-6">
                  <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <Gamepad2 className="w-4 h-4 sm:w-5 sm:h-5" />
                    Game Settings
                  </h3>

                  <div className="space-y-4">
                    <div className="space-y-2">
                      <span className="text-white text-sm sm:text-base">AI Difficulty</span>
                      <div className="grid grid-cols-3 gap-2">
                        {(["easy", "medium", "hard"] as Difficulty[]).map((diff) => (
                          <Button
                            key={diff}
                            variant={settings.difficulty === diff ? "default" : "outline"}
                            size="sm"
                            onClick={() => saveSettings({ ...settings, difficulty: diff })}
                            className={
                              settings.difficulty === diff
                                ? "bg-blue-600 hover:bg-blue-700 text-white text-xs sm:text-sm"
                                : "bg-white/10 border-white/20 text-white hover:bg-white/20 hover:text-white text-xs sm:text-sm"
                            }
                          >
                            {diff.charAt(0).toUpperCase() + diff.slice(1)}
                          </Button>
                        ))}
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-white text-sm sm:text-base">Animations</span>
                      <Switch
                        checked={settings.animations}
                        onCheckedChange={(checked) => saveSettings({ ...settings, animations: checked })}
                      />
                    </div>
                  </div>
                </div>

                {/* Stats Management */}
                <div className="space-y-4 sm:space-y-6">
                  <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <Award className="w-4 h-4 sm:w-5 sm:h-5" />
                    Statistics
                  </h3>

                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-center">
                      <div className="bg-white/5 rounded-lg p-3">
                        <div className="text-xl sm:text-2xl font-bold text-green-400">{gameStats.wins}</div>
                        <div className="text-xs text-green-300">Wins</div>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <div className="text-xl sm:text-2xl font-bold text-orange-400">{gameStats.bestStreak}</div>
                        <div className="text-xs text-orange-300">Best Streak</div>
                      </div>
                    </div>

                    <Button
                      variant="outline"
                      onClick={resetStats}
                      className="w-full bg-red-500/20 border-red-400/30 text-red-300  hover:text-white hover:bg-red-500/30 text-sm"
                    >
                      Reset All Statistics
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  // About Screen
  if (currentScreen === "about") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>
        </div>

        <div className="relative z-10 flex flex-col min-h-screen p-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <Button
              variant="outline"
              onClick={() => setCurrentScreen("menu")}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <h1 className="text-xl sm:text-2xl font-bold text-white text-center">About</h1>
            <div className="w-20"></div>
          </div>

          <div className="flex-1 flex items-center justify-center overflow-y-auto">
            <div className="w-full max-w-2xl space-y-6">
              {/* Creator Card */}
              <Card className="bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl">
                <CardContent className="p-6 sm:p-8">
                  <div className="text-center mb-6 sm:mb-8">
                    <div className="w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center shadow-2xl">
                      <Code className="w-10 h-10 sm:w-12 sm:h-12 text-white" />
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">Created with <span className="text-red-500">❤</span> by Afaq Ul Islam</h2>
                    <p className="text-blue-200 text-base sm:text-lg">Full Stack Developer & Game Enthusiast</p>
                  </div>

                  <div className="space-y-4 sm:space-y-6">
                    {/* Bio */}
                    <div className="text-center">
                      <p className="text-white/90 leading-relaxed text-sm sm:text-base">
                        Passionate full-stack developer specializing in modern web technologies and AI-powered
                        applications. This Tic Tac Toe game demonstrates a complete full-stack architecture with a
                        React/Next.js frontend and Python Flask backend, showcasing both client-side interactivity and
                        server-side game logic with intelligent AI opponents.
                      </p>
                    </div>

                    {/* Tech Stack */}
                    <div className="space-y-4">
                      <h3 className="text-base sm:text-lg font-bold text-white text-center flex items-center justify-center gap-2">
                        <Star className="w-4 h-4 sm:w-5 sm:h-5" />
                        Built With
                      </h3>

                      {/* Frontend Technologies */}
                      <div className="space-y-3">
                        <h4 className="text-sm sm:text-md font-semibold text-blue-300 text-center">Frontend</h4>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3">
                          {[
                            { name: "React", color: "from-blue-400 to-blue-600" },
                            { name: "Next.js", color: "from-gray-400 to-gray-600" },
                            { name: "TypeScript", color: "from-blue-500 to-indigo-600" },
                            { name: "Tailwind CSS", color: "from-cyan-400 to-blue-500" },
                            { name: "Shadcn/ui", color: "from-purple-400 to-pink-500" },
                            { name: "Lucide Icons", color: "from-orange-400 to-red-500" },
                            { name: "Web Audio API", color: "from-green-400 to-emerald-500" },
                            { name: "Local Storage", color: "from-yellow-400 to-orange-500" },
                          ].map((tech) => (
                            <Badge
                              key={tech.name}
                              className={`bg-gradient-to-r ${tech.color} text-white border-0 justify-center py-1 sm:py-2 text-xs`}
                            >
                              {tech.name}
                            </Badge>
                          ))}
                        </div>
                      </div>

                      {/* Backend Technologies */}
                      <div className="space-y-3">
                        <h4 className="text-sm sm:text-md font-semibold text-red-300 text-center">Backend</h4>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3">
                          {[
                            { name: "Python", color: "from-yellow-500 to-blue-500" },
                            { name: "Flask", color: "from-gray-600 to-gray-800" },
                            { name: "Flask-CORS", color: "from-green-500 to-teal-600" },
                            { name: "REST API", color: "from-indigo-500 to-purple-600" },
                            { name: "AI Algorithms", color: "from-pink-500 to-rose-600" },
                            { name: "Game Logic", color: "from-emerald-500 to-green-600" },
                            { name: "Session Control", color: "from-orange-500 to-red-500" },
                            { name: "Random AI", color: "from-violet-500 to-purple-600" },
                          ].map((tech) => (
                            <Badge
                              key={tech.name}
                              className={`bg-gradient-to-r ${tech.color} text-white border-0 justify-center py-1 sm:py-2 text-xs`}
                            >
                              {tech.name}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Features */}
                    <div className="space-y-4">
                      <h3 className="text-base sm:text-lg font-bold text-white text-center flex items-center justify-center gap-2">
                        <Trophy className="w-4 h-4 sm:w-5 sm:h-5" />
                        Game Features
                      </h3>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                        {[
                          { icon: Brain, text: "Smart AI with Multiple Difficulties" },
                          { icon: Volume2, text: "Professional Sound System" },
                          { icon: Award, text: "Statistics & Achievement Tracking" },
                          { icon: Settings, text: "Customizable Game Settings" },
                          { icon: Zap, text: "Smooth Animations & Effects" },
                          { icon: Gamepad2, text: "Professional Game UI/UX" },
                        ].map((feature, index) => (
                          <div key={index} className="flex items-center gap-2 sm:gap-3 text-white/90">
                            <feature.icon className="w-4 h-4 sm:w-5 sm:h-5 text-blue-400 flex-shrink-0" />
                            <span className="text-xs sm:text-sm">{feature.text}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Contact & Links */}
              <Card className="bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl">
                <CardContent className="p-4 sm:p-6">
                  <h3 className="text-base sm:text-lg font-bold text-white text-center mb-4 sm:mb-6 flex items-center justify-center gap-2">
                    <Mail className="w-4 h-4 sm:w-5 sm:h-5" />
                    Connect With Me
                  </h3>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
                    <Button
                      variant="outline"
                      className="bg-white/10 border-white/20 text-white hover:bg-white/20 flex-col h-auto py-3 sm:py-4"
                      onClick={() => window.open("https://github.com/afaqulislam", "_blank")}
                    >
                      <Github className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
                      <span className="text-xs">GitHub</span>
                    </Button>

                    <Button
                      variant="outline"
                      className="bg-white/10 border-white/20 text-white hover:bg-white/20 flex-col h-auto py-3 sm:py-4"
                      onClick={() => window.open("https://www.linkedin.com/in/afaqulislam", "_blank")}
                    >
                      <Linkedin className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
                      <span className="text-xs">LinkedIn</span>
                    </Button>

                    <Button
                      variant="outline"
                      className="bg-white/10 border-white/20 text-white hover:bg-white/20 flex-col h-auto py-3 sm:py-4"
                      onClick={() => window.open("afaqulislam707@gmail.com", "_blank")}
                    >
                      <Mail className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
                      <span className="text-xs">Email</span>
                    </Button>

                    <Button
                      variant="outline"
                      className="bg-white/10 border-white/20 text-white hover:bg-white/20 flex-col h-auto py-3 sm:py-4"
                      onClick={() => window.open("https://aui-portfolio.vercel.app/", "_blank")}
                    >
                      <Globe className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
                      <span className="text-xs">Portfolio</span>
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Fun Facts */}
              <Card className="bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl">
                <CardContent className="p-4 sm:p-6">
                  <h3 className="text-base sm:text-lg font-bold text-white text-center mb-4 sm:mb-6 flex items-center justify-center gap-2">
                    <Coffee className="w-4 h-4 sm:w-5 sm:h-5" />
                    Full-Stack Development Facts
                  </h3>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                    {/* Frontend Stats */}
                    <div className="space-y-4">
                      <h4 className="text-xs sm:text-sm font-semibold text-blue-300 text-center">Frontend</h4>
                      <div className="grid grid-cols-2 gap-3 sm:gap-4 text-center">
                        <div className="space-y-2">
                          <div className="text-xl sm:text-2xl font-bold text-blue-400">800+</div>
                          <div className="text-xs text-white/80">Lines of TSX</div>
                        </div>
                        <div className="space-y-2">
                          <div className="text-xl sm:text-2xl font-bold text-cyan-400">15+</div>
                          <div className="text-xs text-white/80">Components</div>
                        </div>
                      </div>
                    </div>

                    {/* Backend Stats */}
                    <div className="space-y-4">
                      <h4 className="text-xs sm:text-sm font-semibold text-red-300 text-center">Backend</h4>
                      <div className="grid grid-cols-2 gap-3 sm:gap-4 text-center">
                        <div className="space-y-2">
                          <div className="text-xl sm:text-2xl font-bold text-yellow-400">200+</div>
                          <div className="text-xs text-white/80">Lines of Python</div>
                        </div>
                        <div className="space-y-2">
                          <div className="text-xl sm:text-2xl font-bold text-green-400">5+</div>
                          <div className="text-xs text-white/80">API Endpoints</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="text-center mt-4 sm:mt-6 pt-4 border-t border-white/10">
                    <div className="space-y-2">
                      <div className="text-2xl sm:text-3xl font-bold text-purple-400">∞</div>
                      <div className="text-xs sm:text-sm text-white/80">Cups of Coffee ☕</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Thank You */}
              <Card className="bg-gradient-to-r from-pink-500/20 to-purple-500/20 backdrop-blur-xl border-pink-400/30 shadow-2xl">
                <CardContent className="p-4 sm:p-6 text-center">
                  <Heart className="w-6 h-6 sm:w-8 sm:h-8 text-pink-400 mx-auto mb-3 sm:mb-4" />
                  <h3 className="text-base sm:text-lg font-bold text-white mb-2">Thank You for Playing!</h3>
                  <p className="text-white/90 text-xs sm:text-sm">
                    Hope you enjoyed this modern take on the classic Tic Tac Toe game. Feel free to reach out if you
                    have any feedback or suggestions!
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Menu Screen
  if (currentScreen === "menu" && gameMode === null) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 relative overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>
        </div>

        <div className="relative z-10 flex flex-col items-center justify-center min-h-screen p-4">
          {/* Game Logo */}
          <div className="text-center mb-8 sm:mb-12">
            <div className="inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-3xl mb-4 sm:mb-6 shadow-2xl transform rotate-12 hover:rotate-0 transition-transform duration-500">
              <Trophy className="w-10 h-10 sm:w-12 sm:h-12 text-white" />
            </div>
            <h1 className="text-4xl sm:text-6xl font-black text-white mb-2 sm:mb-4 tracking-tight">
              TIC TAC TOE{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">PRO</span>
            </h1>
            <p className="text-lg sm:text-xl text-blue-200 font-medium">Challenge the Ultimate AI</p>
          </div>

          {/* Stats Dashboard */}
          <Card className="w-full max-w-md bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl mb-6 sm:mb-8">
            <CardContent className="p-4 sm:p-6">
              <div className="text-center mb-4 sm:mb-6">
                <h3 className="text-base sm:text-lg font-bold text-white mb-3 sm:mb-4">Your Performance</h3>
                <div className="grid grid-cols-3 gap-3 sm:gap-4">
                  <div className="text-center">
                    <div className="text-xl sm:text-2xl font-bold text-green-400">{gameStats.wins}</div>
                    <div className="text-xs text-green-300">Wins</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl sm:text-2xl font-bold text-red-400">{gameStats.losses}</div>
                    <div className="text-xs text-red-300">Losses</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl sm:text-2xl font-bold text-yellow-400">{gameStats.draws}</div>
                    <div className="text-xs text-yellow-300">Draws</div>
                  </div>
                </div>
              </div>

              {gameStats.streak > 0 && (
                <div className="text-center mb-3 sm:mb-4">
                  <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 sm:px-4 py-1">
                    <Zap className="w-3 h-3 mr-1" />
                    {gameStats.streak} Win Streak!
                  </Badge>
                </div>
              )}

              {gameStats.bestStreak > 0 && (
                <div className="text-center mb-3 sm:mb-4">
                  <div className="text-xs sm:text-sm text-white/80">
                    Best Streak: <span className="text-orange-400 font-bold">{gameStats.bestStreak}</span>
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <div className="flex justify-between text-xs sm:text-sm text-white/80">
                  <span>Win Rate</span>
                  <span>
                    {gameStats.totalGames > 0 ? Math.round((gameStats.wins / gameStats.totalGames) * 100) : 0}%
                  </span>
                </div>
                <Progress
                  value={gameStats.totalGames > 0 ? (gameStats.wins / gameStats.totalGames) * 100 : 0}
                  className="h-2 bg-white/20"
                />
              </div>

              <div className="text-center mt-3 sm:mt-4">
                <div className="text-xs text-white/60">
                  Difficulty: <span className="text-blue-300 capitalize">{settings.difficulty}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Play Buttons */}
          <div className="space-y-4 w-full max-w-md">
            <Button
              onClick={() => initializeGame("ai")}
              disabled={loading}
              className="w-full h-14 sm:h-16 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white text-lg sm:text-xl font-bold rounded-2xl shadow-2xl hover:shadow-green-500/25 transition-all duration-300 hover:scale-105"
            >
              {loading ? (
                <div className="flex items-center gap-3">
                  <div className="w-5 h-5 sm:w-6 sm:h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Starting Game...
                </div>
              ) : (
                <div className="flex items-center gap-3">
                  <Brain className="w-5 h-5 sm:w-6 sm:h-6" />
                  Challenge AI
                </div>
              )}
            </Button>

            <Button
              onClick={() => initializeGame("human")}
              disabled={loading}
              className="w-full h-14 sm:h-16 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white text-lg sm:text-xl font-bold rounded-2xl shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 hover:scale-105"
            >
              {loading ? (
                <div className="flex items-center gap-3">
                  <div className="w-5 h-5 sm:w-6 sm:h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Starting Game...
                </div>
              ) : (
                <div className="flex items-center gap-3">
                  <User className="w-5 h-5 sm:w-6 sm:h-6" />
                  Play with Friend
                </div>
              )}
            </Button>
          </div>

          {/* Secondary Actions */}
          <div className="flex gap-3 sm:gap-4 mt-6">
            <Button
              variant="outline"
              onClick={() => setCurrentScreen("settings")}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-sm sm:text-base"
            >
              <Settings className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
              Settings
            </Button>
            <Button
              variant="outline"
              onClick={() => setCurrentScreen("about")}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-sm sm:text-base"
            >
              <Info className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
              About
            </Button>
            <Button
              variant="outline"
              onClick={() => saveSettings({ ...settings, soundEnabled: !settings.soundEnabled })}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20"
            >
              {settings.soundEnabled ? (
                <Volume2 className="w-3 h-3 sm:w-4 sm:h-4" />
              ) : (
                <VolumeX className="w-3 h-3 sm:w-4 sm:h-4" />
              )}
            </Button>
          </div>
        </div>
      </div>
    )
  }

  // Loading Screen
  if (loading || initialLoading) {
    return <BeautifulLoader message="Preparing Battle Arena" />
  }

  // Error Screen
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
        <Card className="w-full max-w-lg bg-white/10 backdrop-blur-xl border-white/20 shadow-2xl">
          <CardContent className="p-8 sm:p-12 text-center">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6">
              <Target className="w-8 h-8 sm:w-10 sm:h-10 text-red-400" />
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white mb-3 sm:mb-4">Connection Failed</h2>
            <p className="text-blue-200 mb-6 sm:mb-8 leading-relaxed text-sm sm:text-base">{error}</p>
            <div className="flex gap-3 sm:gap-4 justify-center">
              <Button
                onClick={() => initializeGame("ai")}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-sm sm:text-base"
              >
                Retry
              </Button>
              <Button
                variant="outline"
                onClick={() => setCurrentScreen("menu")}
                className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-sm sm:text-base"
              >
                <Home className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
                Menu
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Initial Loading Screen
  if (initialLoading) {
    return <InitialLoader />
  }

  // Game Screen
  if (!gameState) return null

  // Game Screen
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 relative overflow-hidden">
      {/* Result Popup */}
      {showResultPopup && gameResult && (
        <ResultPopup
          result={gameResult}
          onClose={() => setShowResultPopup(false)}
          gameMode={gameMode || "ai"}
          currentPlayer={currentPlayer}
        />
      )}

      {/* Game Result Animation */}
      {gameResult && settings.animations && !showResultPopup}

      {/* Celebration Effect */}
      {showCelebration && settings.animations && (
        <div className="absolute inset-0 z-40 pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/20 to-orange-500/20 animate-pulse"></div>
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-yellow-400 rounded-full animate-bounce"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${1 + Math.random()}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 flex flex-col min-h-screen p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-4 sm:mb-6">
          <Button
            variant="outline"
            onClick={() => {
              setCurrentScreen("menu")
              setGameMode(null)
              setGameState(null)
            }}
            className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-sm sm:text-base"
          >
            <Home className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
            Menu
          </Button>

          <div className="text-center">
            <h1 className="text-lg sm:text-2xl font-bold text-white">Battle Arena</h1>
            <p className="text-blue-200 text-xs sm:text-sm">
              {gameMode === "human"
                ? "Human vs Human"
                : `Round ${gameStats.totalGames + 1} • ${settings.difficulty.charAt(0).toUpperCase() + settings.difficulty.slice(1)} AI`}
            </p>
          </div>

          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => saveSettings({ ...settings, soundEnabled: !settings.soundEnabled })}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20"
            >
              Volume
              {settings.soundEnabled ? (
                <Volume2 className="w-3 h-3 sm:w-4 sm:h-4" />
              ) : (
                <VolumeX className="w-3 h-3 sm:w-4 sm:h-4" />
              )}
            </Button>
          </div>
        </div>

        {/* Players */}
        <div className="flex justify-between items-center mb-6 sm:mb-8">
          <div className="flex items-center gap-2 sm:gap-3">
            <Avatar className="w-10 h-10 sm:w-12 sm:h-12 border-2 border-blue-400">
              <AvatarFallback className="bg-blue-500 text-white">
                <User className="w-5 h-5 sm:w-6 sm:h-6" />
              </AvatarFallback>
            </Avatar>
            <div>
              <div className="text-white font-bold text-sm sm:text-base">
                {gameMode === "human" ? "Player 1" : "You"}
              </div>
              <div className="text-blue-300 text-xs sm:text-sm">Player X</div>
            </div>
          </div>

          <div className="text-center">
            <div className="text-2xl sm:text-4xl font-bold text-white mb-1">VS</div>
            {!gameState.game_over && (
              <div className="min-h-[24px] flex items-center justify-center">
                {aiThinking && gameMode === "ai" ? (
                  <AIThinkingIndicator />
                ) : (
                  <div
                    className={`text-xs sm:text-sm px-2 sm:px-3 py-1 rounded-full ${gameMode === "human"
                      ? currentPlayer === "X"
                        ? "bg-blue-500/20 text-blue-300 border border-blue-500/30"
                        : "bg-red-500/20 text-red-300 border border-red-500/30"
                      : gameState.player_turn === "X"
                        ? "bg-blue-500/20 text-blue-300 border border-blue-500/30"
                        : "bg-red-500/20 text-red-300 border border-red-500/30"
                      }`}
                  >
                    {makingMove
                      ? "Processing..."
                      : gameMode === "human"
                        ? `Player ${currentPlayer}'s Turn`
                        : gameState.player_turn === "X"
                          ? "Your Turn"
                          : "AI Turn"}
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            <div className="text-right">
              <div className="text-white font-bold text-sm sm:text-base">
                {gameMode === "human" ? "Player 2" : "AI Bot"}
              </div>
              <div className="text-red-300 text-xs sm:text-sm">Player O</div>
            </div>
            <Avatar className="w-10 h-10 sm:w-12 sm:h-12 border-2 border-red-400">
              <AvatarFallback className="bg-red-500 text-white">
                {gameMode === "human" ? (
                  <User className="w-5 h-5 sm:w-6 sm:h-6" />
                ) : (
                  <Bot className="w-5 h-5 sm:w-6 sm:h-6" />
                )}
              </AvatarFallback>
            </Avatar>
          </div>
        </div>

        {/* Game Status */}
        {gameState.status && (
          <div className="text-center mb-4 sm:mb-6">
            <div
              className={`inline-block px-4 sm:px-8 py-2 sm:py-4 rounded-xl sm:rounded-2xl shadow-2xl ${gameState.status.includes("Win") || gameState.status.includes("Player")
                ? "bg-gradient-to-r from-green-500 to-emerald-600 text-white"
                : gameState.status.includes("AI Wins")
                  ? "bg-gradient-to-r from-red-500 to-pink-600 text-white"
                  : "bg-gradient-to-r from-yellow-500 to-orange-600 text-white"
                }`}
            >
              <h2 className="text-lg sm:text-2xl font-bold">{gameState.status}</h2>
            </div>
          </div>
        )}

        {/* Game Board */}
        <div className="flex-1 flex items-center justify-center mb-6 sm:mb-8">
          <div className="relative">
            <div className="grid grid-cols-3 gap-2 sm:gap-4 p-4 sm:p-8 bg-white/10 backdrop-blur-xl rounded-2xl sm:rounded-3xl border border-white/20 shadow-2xl">
              {gameState.board &&
                gameState.board.map((row, i) =>
                  row.map((cell, j) => {
                    const cellKey = `${i}-${j}`
                    const isAnimating = animatingCell === cellKey && settings.animations
                    const isWinning = winningCells.includes(cellKey)

                    const canMove =
                      gameMode === "human"
                        ? cell === "" && !gameState.game_over && !makingMove
                        : cell === "" &&
                        !gameState.game_over &&
                        gameState.player_turn === "X" &&
                        !makingMove &&
                        !aiThinking

                    return (
                      <button
                        key={cellKey}
                        onClick={() => makeMove(i, j)}
                        disabled={!canMove}
                        className={`
                        relative w-16 h-16 sm:w-24 sm:h-24 text-2xl sm:text-3xl font-black rounded-xl sm:rounded-2xl border-2 transition-all duration-300 group
                        ${canMove
                            ? "bg-white/20 border-white/30 hover:border-blue-400 hover:bg-blue-500/20 cursor-pointer hover:scale-110 hover:shadow-2xl"
                            : "cursor-not-allowed"
                          }
                        ${cell === "X" ? "bg-blue-500/30 border-blue-400 text-blue-300 shadow-lg shadow-blue-500/25" : ""}
                        ${cell === "O" ? "bg-red-500/30 border-red-400 text-red-300 shadow-lg shadow-red-500/25" : ""}
                        ${cell === "" ? "bg-white/10 border-white/20" : ""}
                        ${isAnimating ? "scale-125 shadow-2xl" : ""}
                        ${isWinning ? "ring-4 ring-yellow-400 ring-opacity-75 bg-yellow-500/30 animate-pulse" : ""}
                        ${makingMove || aiThinking ? "opacity-50" : ""}
                      `}
                      >
                        <span className={`${isAnimating ? "animate-bounce" : ""} ${isWinning ? "animate-pulse" : ""}`}>
                          {cell}
                        </span>

                        {/* Hover Preview */}
                        {canMove && (
                          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-40 transition-opacity duration-200">
                            <span className="text-blue-400 text-xl sm:text-2xl font-black">
                              {gameMode === "human" ? currentPlayer : "X"}
                            </span>
                          </div>
                        )}

                        {/* Glow Effect for Winning Cells */}
                        {isWinning && settings.animations && (
                          <div className="absolute inset-0 bg-yellow-400/20 rounded-xl sm:rounded-2xl animate-pulse"></div>
                        )}
                      </button>
                    )
                  }),
                )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-3 sm:gap-4">
          <Button
            onClick={resetGame}
            disabled={loading || makingMove || aiThinking}
            className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold px-6 sm:px-8 py-2 sm:py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 text-sm sm:text-base"
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 sm:w-4 sm:h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Loading...
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <RotateCcw className="w-3 h-3 sm:w-4 sm:h-4" />
                New Round
              </div>
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}
