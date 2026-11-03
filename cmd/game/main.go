// Command game is the WebAssembly entry point for Spirit Space.
// It is the only package allowed to touch the DOM (Constitution, Law 5).
package main

import (
	"fmt"
	"syscall/js"

	"spirit-space/internal/game"
)

func main() {
	doc := js.Global().Get("document")
	canvas := doc.Call("getElementById", "game")
	ctx := canvas.Call("getContext", "2d")

	g := game.New()
	input := game.Input{}

	// Input capture: keydown/keyup update the shared input state.
	// No game rule lives here (Constitution, Law 1).
	const (
		keyLeft  = "ArrowLeft"
		keyRight = "ArrowRight"
		keyUp    = "ArrowUp"
		keyDown  = "ArrowDown"
		keyA     = "KeyA"
		keyD     = "KeyD"
		keyW     = "KeyW"
		keyS     = "KeyS"
		keySpace = "Space"
		keyR     = "KeyR"
	)

	mapKey := func(code string) *bool {
		switch code {
		case keyLeft, keyA:
			return &input.Left
		case keyRight, keyD:
			return &input.Right
		case keyUp, keyW:
			return &input.Up
		case keyDown, keyS:
			return &input.Down
		case keySpace:
			return &input.Fire
		}
		return nil
	}

	doc.Call("addEventListener", "keydown", js.FuncOf(func(_ js.Value, args []js.Value) any {
		e := args[0]
		if p := mapKey(e.Get("code").String()); p != nil {
			*p = true
			e.Call("preventDefault")
		}
		if e.Get("code").String() == keyR && g.GameOver {
			g.Restart()
		}
		return nil
	}))
	doc.Call("addEventListener", "keyup", js.FuncOf(func(_ js.Value, args []js.Value) any {
		if p := mapKey(args[0].Get("code").String()); p != nil {
			*p = false
		}
		return nil
	}))

	var last float64
	var render js.Func

	// frame reads state and draws it; it never mutates the simulation
	// except by calling Update (Constitution, Law 2).
	frame := func(this js.Value, args []js.Value) any {
		now := args[0].Float() / 1000.0 // ms → s
		dt := now - last
		last = now
		if dt > 0.1 {
			dt = 0.1 // clamp long pauses so the sim stays stable
		}
		g.SetInput(input)
		g.Update(dt)
		draw(ctx, g)
		js.Global().Call("requestAnimationFrame", render) // re-arm the loop
		return nil
	}
	render = js.FuncOf(frame)
	js.Global().Call("requestAnimationFrame", render)

	select {} // keep the WASM instance alive
}

// draw renders the current game state to the canvas.
func draw(ctx js.Value, g *game.Game) {
	ctx.Set("fillStyle", "#000")
	ctx.Call("fillRect", 0, 0, game.Width, game.Height) // black background
	ctx.Set("fillStyle", "#fff")

	// Player: triangle-ish ship (a circle here, kept simple).
	ctx.Call("beginPath")
	ctx.Call("arc", g.Player.X, g.Player.Y, g.Player.Radius, 0, 6.283)
	ctx.Call("fill")

	// Bullets: small squares.
	for _, b := range g.Bullets {
		ctx.Call("fillRect", b.X-2, b.Y-2, 4, 4)
	}

	// Enemies: circles.
	for _, e := range g.Enemies {
		ctx.Call("beginPath")
		ctx.Call("arc", e.X, e.Y, e.Radius, 0, 6.283)
		ctx.Call("fill")
	}

	// HUD: score, or the game-over banner.
	if g.GameOver {
		ctx.Call("fillText", "GAME OVER — press R to restart", 280, 300)
	} else {
		ctx.Call("fillText", fmt.Sprintf("Score: %d", g.Score), 10, 20)
	}
}
