"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Trophy, Frown, Handshake, X, Sparkles } from "lucide-react"

interface ResultPopupProps {
  result: "win" | "lose" | "draw"
  onClose: () => void
  gameMode: "ai" | "human"
  currentPlayer?: "X" | "O"
}

export function ResultPopup({ result, onClose, gameMode, currentPlayer }: ResultPopupProps) {
  const getConfig = () => {
    const opponent = currentPlayer === "X" ? "O" : "X";

    if (gameMode === "human") {
      if (result === "win") {
        return {
          icon: Trophy,
          title: `Player ${currentPlayer} Wins!`,
          subtitle: `You defeated Player ${opponent}.`,
          bgColor: "from-green-500/20 to-emerald-500/20",
          borderColor: "border-green-400/30",
          iconColor: "text-green-400",
          buttonColor: "from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700",
        };
      } else if (result === "lose") {
        return {
          icon: Trophy,
          title: `Player ${opponent} Wins!`,
          subtitle: `Player ${currentPlayer} was defeated.`,
          bgColor: "from-blue-500/20 to-purple-500/20",
          borderColor: "border-blue-400/30",
          iconColor: "text-blue-400",
          buttonColor: "from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700",
        };
      } else {
        return {
          icon: Handshake,
          title: "It's a Draw!",
          subtitle: "Great match, both players!",
          bgColor: "from-yellow-500/20 to-orange-500/20",
          borderColor: "border-yellow-400/30",
          iconColor: "text-yellow-400",
          buttonColor: "from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700",
        };
      }
    } else {
      // AI Mode
      if (result === "win") {
        return {
          icon: Trophy,
          title: "Victory!",
          subtitle: "You defeated the AI!",
          bgColor: "from-green-500/20 to-emerald-500/20",
          borderColor: "border-green-400/30",
          iconColor: "text-green-400",
          buttonColor: "from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700",
        };
      } else if (result === "lose") {
        return {
          icon: Frown,
          title: "Defeat",
          subtitle: "AI wins this round!",
          bgColor: "from-red-500/20 to-pink-500/20",
          borderColor: "border-red-400/30",
          iconColor: "text-red-400",
          buttonColor: "from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700",
        };
      } else {
        return {
          icon: Handshake,
          title: "Draw!",
          subtitle: "Great match!",
          bgColor: "from-yellow-500/20 to-orange-500/20",
          borderColor: "border-yellow-400/30",
          iconColor: "text-yellow-400",
          buttonColor: "from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700",
        };
      }
    }
  };



  const config = getConfig()
  const IconComponent = config.icon

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      {/* Floating particles for win */}
      {result === "win" && (
        <>
          {[...Array(15)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-green-400 rounded-full animate-bounce opacity-80 pointer-events-none"
              style={{
                left: `${20 + Math.random() * 60}%`,
                top: `${20 + Math.random() * 60}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${1 + Math.random()}s`,
              }}
            />
          ))}
          <Sparkles className="absolute top-1/4 left-1/4 w-8 h-8 text-yellow-400 animate-pulse pointer-events-none" />
          <Sparkles className="absolute top-1/3 right-1/4 w-6 h-6 text-green-400 animate-pulse delay-500 pointer-events-none" />
          <Sparkles className="absolute bottom-1/3 left-1/3 w-10 h-10 text-blue-400 animate-pulse delay-1000 pointer-events-none" />
        </>
      )}

      {/* Result card */}
      <Card
        className={`relative bg-gradient-to-br ${config.bgColor} backdrop-blur-xl ${config.borderColor} border-2 shadow-2xl animate-in zoom-in-50 duration-500 max-w-md w-full`}
      >
        {/* Close button */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onClose}
          className="absolute top-4 right-4 text-white/60 hover:text-white hover:bg-white/10 rounded-full w-8 h-8 p-0"
        >
          <X className="w-4 h-4" />
        </Button>

        <CardContent className="p-8 text-center">
          <div className="mb-6">
            <div
              className={`w-20 h-20 mx-auto rounded-full bg-white/10 flex items-center justify-center mb-4 ${result === "win" ? "animate-bounce" : "animate-pulse"}`}
            >
              <IconComponent className={`w-12 h-12 ${config.iconColor}`} />
            </div>
          </div>

          <h2 className="text-3xl font-bold text-white mb-2">{config.title}</h2>
          <p className="text-white/80 text-lg mb-6">{config.subtitle}</p>

          <Button
            onClick={onClose}
            className={`w-full bg-gradient-to-r ${config.buttonColor} text-white font-bold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105`}
          >
            Continue Playing
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
