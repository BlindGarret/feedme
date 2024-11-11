package main

import (
	"fmt"
	"net/http"

	"github.com/BlindGarret/echorend/gatherers/glob"
	"github.com/BlindGarret/echorend/renderers/handlebars"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	viewDir := "templates/pages"
	partialsDir := "templates/components"
	viewGatherer := glob.NewGlobGatherer(glob.GlobGathererConfig{
		TemplateDir:     &viewDir,
		IncludeTLDInKey: false,
		Extensions:      []string{".hbs"},
	})

	partialGatherer := glob.NewGlobGatherer(glob.GlobGathererConfig{
		TemplateDir:     &partialsDir,
		IncludeTLDInKey: false,
		Extensions:      []string{".hbs"},
	})

	renderer := handlebars.NewHandlebarsRenderer(viewGatherer, partialGatherer)
	renderer.MustSetup()
	errs := renderer.CheckRenders()
	if len(errs) > 0 {
		for _, err := range errs {
			fmt.Println(err)
		}
		return
	}

	e := echo.New()

	e.Static("/public", "public")
	e.Use(middleware.GzipWithConfig(middleware.GzipConfig{
		Level: 1,
	}))

	e.Renderer = renderer

	e.GET("/", func(c echo.Context) error {
		return c.Render(http.StatusOK, "index", map[string]interface{}{
			"Title": "Hello, World!",
		})
	})

	e.GET("/partial", func(c echo.Context) error {
		return c.Render(http.StatusOK, "test_component", map[string]interface{}{
			"Title": "Just the partial now",
		})
	})

	e.Logger.Fatal(e.Start(":1323"))
}
