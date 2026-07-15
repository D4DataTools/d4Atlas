from pathlib import Path

def write_atlas_html(borders, markers, path):
    image_url = "https://files.blizzhackers.dev/d4tex/Sanctuary_Eastern_Continent_map.jpg"

    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
              rel="stylesheet">

        <script src="https://unpkg.com/panzoom@9.4.0/dist/panzoom.min.js"></script>

        <link href="atlas.css" rel="stylesheet">

        <style id="dynamic-css"></style>
    </head>

    <body>

    <div class="search-input">
        <input
            type="search"
            id="search-input"
            class="form-control"
            placeholder="Search..."
            value="dungeon location">
    </div>

    <svg
        viewBox="-1284 -2618 3564 3564"
        xmlns="http://www.w3.org/2000/svg"
        style="width:100%;height:100%;">

        <g
            id="atlas-group"
            transform="matrix(3.6466190067585558 0 0 3.6466190067585558 -3030 3625)">

            <image
                href="{image_url}"
                x="-1356"
                y="-2724"
                width="3836"
                height="3836">

                <title>Sanctuary Eastern Continent</title>

            </image>

            <g transform="scale(-1,1) rotate(45)">

    {"".join("            " + b + "\n" for b in borders)}

    {"".join("            " + m + "\n" for m in markers)}

            </g>

        </g>

    </svg>

    <script src="atlas.js"></script>

    </body>
    </html>
    """

    Path("docs").mkdir(exist_ok=True)

    Path("docs/atlas.html").write_text(html, encoding="utf-8")





        return




# fs.writeFileSync('docs/atlas.html', `<html>
#   <head>
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
#     <script src='https://unpkg.com/panzoom@9.4.0/dist/panzoom.min.js'></script>
#     <link href="atlas.css" rel="stylesheet">
#     <style id="dynamic-css"></style>
#   </head>
#   <body>
#     <div class="search-input">
#       <input type="search" id="search-input" class="form-control" placeholder="Search..." value="dungeon location">
#     </div>
#     <svg viewBox="-1284 -2618 3564 3564" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
#       <g id="atlas-group" transform="matrix(3.6466190067585558 0 0 3.6466190067585558 -3030 3625)">
#         <image href="${imageUrl}" x="-1356" y="-2724" width="3836" height="3836">
#           <title>Sanctuary Eastern Continent</title>
#         </image>
#         <g transform="scale(-1, 1) rotate(45)">
#           ${borders.join('\n          ')}
#           ${markers.join('\n          ')}
#         </g>
#       </g>
#     </svg>
#     <script src="atlas.js"></script>
#   </body>
# </html>`);