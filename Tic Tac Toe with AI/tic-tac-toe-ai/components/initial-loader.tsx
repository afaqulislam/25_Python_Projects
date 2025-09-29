"use client"

import { useEffect, useState } from "react"
import { Trophy, Zap, Brain, Sparkles } from "lucide-react"

export function InitialLoader() {
  const [progress, setProgress] = useState(0)
  const [currentText, setCurrentText] = useState("Initializing Game Engine...")

  const loadingTexts = [
    "Initializing Game Engine...",
    "Loading AI Intelligence...",
    "Preparing Battle Arena...",
    "Ready to Play!",
  ]

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval)
          return 100
        }
        return prev + 2
      })
    }, 60)

    const textInterval = setInterval(() => {
      setCurrentText((prev) => {
        const currentIndex = loadingTexts.indexOf(prev)
        const nextIndex = (currentIndex + 1) % loadingTexts.length
        return loadingTexts[nextIndex]
      })
    }, 750)

    return () => {
      clearInterval(progressInterval)
      clearInterval(textInterval)
    }
  }, [])

  return (
    <div className="fixed inset-0 z-50 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-indigo-500/20 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      {/* Floating Icons */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute animate-float opacity-20"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 2}s`,
            }}
          >
            {i % 4 === 0 && <Trophy className="w-8 h-8 text-yellow-400" />}
            {i % 4 === 1 && <Zap className="w-8 h-8 text-blue-400" />}
            {i % 4 === 2 && <Brain className="w-8 h-8 text-purple-400" />}
            {i % 4 === 3 && <Sparkles className="w-8 h-8 text-pink-400" />}
          </div>
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 text-center p-8">
        {/* Logo */}
        <div className="mb-8">
          <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full shadow-2xl animate-bounce">
            <Trophy className="w-16 h-16 text-white" />
          </div>
        </div>

        {/* Title */}
        <h1 className="text-6xl font-black text-white mb-4 tracking-tight animate-pulse">
          TIC TAC{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">PRO</span>
        </h1>

        {/* Loading Text */}
        <p className="text-xl text-blue-200 mb-8 animate-fade-in">{currentText}</p>

        {/* Progress Bar */}
        <div className="w-80 mx-auto mb-6">
          <div className="bg-white/20 rounded-full h-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-full rounded-full transition-all duration-300 ease-out relative"
              style={{ width: `${progress}%` }}
            >
              <div className="absolute inset-0 bg-white/30 animate-pulse"></div>
            </div>
          </div>
          <div className="text-center mt-2 text-white/80 text-sm">{progress}%</div>
        </div>

        {/* Loading Dots */}
        <div className="flex justify-center space-x-2">
          <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce delay-100"></div>
          <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce delay-200"></div>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
        @keyframes fade-in {
          0% { opacity: 0; transform: translateY(10px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-float {
          animation: float 4s ease-in-out infinite;
        }
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
      `}</style>
    </div>
  )
}
