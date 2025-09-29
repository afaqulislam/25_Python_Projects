import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AUI TIC TAC TOE AI GAME',
  description: 'Tic-Tac-Toe game with AI and multiplayer modes, built using Next.js and Radix UI on the frontend, with a Python-powered backend. Created by AUI.',
  generator: 'NEXTJS',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
