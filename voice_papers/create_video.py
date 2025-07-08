#!/usr/bin/env python3
"""Script to create vertical videos from audio files."""

import click
from pathlib import Path
from voice_papers.video import create_vertical_video, create_horizontal_video


@click.command()
@click.argument("audio_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output video path (defaults to audio_path with .mp4 extension)",
)
@click.option(
    "--background-keywords",
    "-k",
    default="abstract,gradient,minimal",
    help="Keywords for Unsplash background image",
)
@click.option(
    "--waveform-style",
    "-w",
    default="circular",
    type=click.Choice(
        [
            "circular",
            "sine",
            "mathematical",
            "fractal",
            "julia",
            "mandelbrot",
            "psychedelic",
            "circles",
            "fluid",
            "liquid",
            "particles",
            "sand",
            "morph",
            "shapes",
            "kaleidoscope",
            "mirror",
            "k-mandala",
            "k-crystal",
            "k-flower",
            "k-sacred",
            "k-tribal",
            "k-laser",
            "k-web",
            "k-spiral",
            "k-diamond",
            "k-stars",
            "breathing",
            "zen",
            "matrix",
            "rain",
            "starfield",
            "space",
            "network",
            "web",
            "swarm",
            "flock",
            "explosion",
            "fireworks",
        ]
    ),
    help="Waveform visualization style: circular (bars), sine (waves), mathematical/fractal (math forms), julia/mandelbrot (fractal zoom), psychedelic/circles (zoom psicodélico), fluid/liquid (ondas fluidas), particles/sand (partículas), morph/shapes (formas que cambian), kaleidoscope/mirror (caleidoscopio), k-mandala (mandalas geométricos), k-crystal (cristales fractales), k-flower (flores simétricas), k-sacred (geometría sagrada), k-tribal (patrones tribales), k-laser (rayos láser), k-web (telarañas simétricas), k-spiral (espirales múltiples), k-diamond (diamantes cristalinos), k-stars (estrellas multicapa), breathing/zen (respiración zen), matrix/rain (lluvia digital Matrix), starfield/space (campo de estrellas denso), network/web (red de conexiones), swarm/flock (enjambre de partículas), explosion/fireworks (fuegos artificiales)",
)
@click.option(
    "--gradient-style",
    "-g",
    default="default",
    type=click.Choice(
        [
            "default",
            "dark_teal_orange",
            "sunset",
            "ocean",
            "purple_pink",
            "forest",
            "midnight",
            "fire",
            "arctic",
            "cosmic",
            "cherry_blossom",
            "tropical",
            "lavender_mist",
            "golden_hour",
            "emerald_sea",
            "rose_gold",
            "northern_lights",
            "desert_sand",
            "deep_ocean",
            "neon_cyber",
            "autumn_leaves",
            "moonlight",
            "tropical_sunset",
            "winter_frost",
            "sakura_dream",
            "volcanic",
            "electric_blue",
            "jungle_green",
            "royal_purple",
            "cotton_candy",
        ]
    ),
    help="Background gradient style (used when Unsplash image fails)",
)
@click.option(
    "--custom-colors",
    "-c",
    help="Custom gradient colors as comma-separated RGB values: '255,0,0,0,255,0,0,0,255' for red-green-blue gradient",
)
@click.option(
    "--no-unsplash",
    is_flag=True,
    help="Skip Unsplash download and use only gradient background",
)
@click.option(
    "--dynamic-background",
    "--db",
    default="none",
    type=click.Choice(
        [
            "none",
            "flowing-gradient",
            "nebula",
            "aurora",
            "plasma",
            "liquid-metal",
            "cosmic-dust",
            "energy-waves",
            "particle-field",
            "morphing-shapes",
            "breathing-colors",
        ]
    ),
    help="Fondo dinámico animado: none (estático), flowing-gradient (gradiente fluido), nebula (nebulosa espacial), aurora (aurora boreal), plasma (plasma energético), liquid-metal (metal líquido), cosmic-dust (polvo cósmico), energy-waves (ondas de energía), particle-field (campo de partículas), morphing-shapes (formas que cambian), breathing-colors (colores que respiran)",
)
@click.option(
    "--orientation",
    "-r",
    default="vertical",
    type=click.Choice(["vertical", "horizontal"]),
    help="Video orientation: vertical (1080x1920) or horizontal (1920x1080)",
)
@click.option(
    "--preview",
    "-p",
    is_flag=True,
    help="Create a 10-second preview instead of full video",
)
@click.option(
    "--particle-colors",
    "--pc",
    default="multicolor",
    type=click.Choice(
        ["multicolor", "background", "dissonant", "triadic", "monochrome"]
    ),
    help="Esquema de colores para partículas: multicolor (arcoíris), background (similar al fondo), dissonant (contrastante), triadic (triada complementaria), monochrome (usa exactamente los colores del fondo)",
)
@click.option(
    "--particle-gradient",
    "--pg",
    type=click.Choice(
        [
            "default",
            "dark_teal_orange",
            "sunset",
            "ocean",
            "purple_pink",
            "forest",
            "midnight",
            "fire",
            "arctic",
            "cosmic",
            "cherry_blossom",
            "tropical",
            "lavender_mist",
            "golden_hour",
            "emerald_sea",
            "rose_gold",
            "northern_lights",
            "desert_sand",
            "deep_ocean",
            "neon_cyber",
            "autumn_leaves",
            "moonlight",
            "tropical_sunset",
            "winter_frost",
            "sakura_dream",
            "volcanic",
            "electric_blue",
            "jungle_green",
            "royal_purple",
            "cotton_candy",
        ]
    ),
    help="Gradiente específico para partículas (independiente del fondo) - solo funciona con --particle-colors background o monochrome",
)
@click.option(
    "--particle-custom-colors",
    "--pcc",
    help="Colores personalizados para partículas como valores RGB separados por comas: '255,0,0,0,255,0,0,0,255' para gradiente rojo-verde-azul",
)
def main(
    audio_path: Path,
    output: Path,
    background_keywords: str,
    waveform_style: str,
    gradient_style: str,
    custom_colors: str,
    no_unsplash: bool,
    dynamic_background: str,
    orientation: str,
    preview: bool,
    particle_colors: str,
    particle_gradient: str,
    particle_custom_colors: str,
):
    """Create a video from an audio file with animated waveform.

    Supports both vertical (1080x1920) and horizontal (1920x1080) orientations.
    """

    # Determine output path
    if not output:
        preview_suffix = "_preview" if preview else ""
        output = (
            audio_path.parent / f"{audio_path.stem}_{orientation}{preview_suffix}.mp4"
        )

    resolution = "1080x1920" if orientation == "vertical" else "1920x1080"
    duration_text = "10-second preview" if preview else "full video"
    click.echo(
        f"🎬 Creating {orientation} {duration_text} ({resolution}) from: {audio_path.name}"
    )
    click.echo(f"📁 Output: {output}")
    click.echo(f"🖼️  Background keywords: {background_keywords}")
    click.echo(f"〰️  Waveform style: {waveform_style}")
    click.echo(f"🌈  Gradient style: {gradient_style}")
    click.echo(f"🎨  Particle colors: {particle_colors}")
    if dynamic_background != "none":
        click.echo(f"🌊  Dynamic background: {dynamic_background}")
    if particle_gradient:
        click.echo(f"🌈  Particle gradient: {particle_gradient}")
    if particle_custom_colors:
        click.echo(f"🎨  Particle custom colors: {particle_custom_colors}")
    if preview:
        click.echo(f"⏱️  Preview mode: 10 seconds maximum")
    if custom_colors:
        click.echo(f"🎨  Custom colors: {custom_colors}")

    # Parse custom colors if provided
    parsed_colors = None
    if custom_colors:
        try:
            # Parse comma-separated RGB values: "255,0,0,0,255,0,0,0,255"
            color_values = [int(x.strip()) for x in custom_colors.split(",")]
            if len(color_values) % 3 == 0 and len(color_values) >= 6:
                parsed_colors = [
                    (color_values[i], color_values[i + 1], color_values[i + 2])
                    for i in range(0, len(color_values), 3)
                ]
                click.echo(f"✅  Parsed {len(parsed_colors)} colors successfully")
            else:
                click.echo(
                    "⚠️  Custom colors format invalid (need multiple sets of 3 RGB values)"
                )
        except ValueError:
            click.echo(
                "⚠️  Custom colors format invalid (values must be integers 0-255)"
            )

    # Parse particle custom colors if provided
    parsed_particle_colors = None
    if particle_custom_colors:
        try:
            # Parse comma-separated RGB values: "255,0,0,0,255,0,0,0,255"
            color_values = [int(x.strip()) for x in particle_custom_colors.split(",")]
            if len(color_values) % 3 == 0 and len(color_values) >= 6:
                parsed_particle_colors = [
                    (color_values[i], color_values[i + 1], color_values[i + 2])
                    for i in range(0, len(color_values), 3)
                ]
                click.echo(
                    f"✅  Parsed {len(parsed_particle_colors)} particle colors successfully"
                )
            else:
                click.echo(
                    "⚠️  Particle custom colors format invalid (need multiple sets of 3 RGB values)"
                )
        except ValueError:
            click.echo(
                "⚠️  Particle custom colors format invalid (values must be integers 0-255)"
            )

    # Create the video with specified orientation
    if orientation == "horizontal":
        success = create_horizontal_video(
            audio_path,
            output,
            background_keywords,
            waveform_style,
            gradient_style,
            parsed_colors,
            no_unsplash,
            dynamic_background,
            preview_duration=10.0 if preview else None,
            particle_color_scheme=particle_colors,
            particle_gradient_style=particle_gradient,
            particle_custom_colors=parsed_particle_colors,
        )
    else:
        success = create_vertical_video(
            audio_path,
            output,
            background_keywords,
            waveform_style,
            gradient_style,
            parsed_colors,
            no_unsplash,
            dynamic_background,
            orientation,
            preview_duration=10.0 if preview else None,
            particle_color_scheme=particle_colors,
            particle_gradient_style=particle_gradient,
            particle_custom_colors=parsed_particle_colors,
        )

    if success:
        click.echo(f"✅ Video created successfully!")
        click.echo(f"📹 Video saved to: {output}")
    else:
        click.echo("❌ Failed to create video")
        raise click.Abort()


if __name__ == "__main__":
    main()
