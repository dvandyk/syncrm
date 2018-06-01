#!/usr/bin/python
# vim: set sw=4 sts=4 et tw=120 :

import struct

class LinesFile:
    def __init__(self, input_file):
        self.input_file = input_file
        # Size
        self.x_width = 1404
        self.y_width = 1872
        # Color mappings
        self.stroke_color = {
            0: 'black',
            1: 'grey',
            2: 'white',
            3: 'yellow'
        }


    def to_svg(self, output, colored = False):
        # Read the file in memory. Consider optimising by reading chunks.
        with open(self.input_file, 'rb') as f:
            data = f.read()
        offset = 0

        # Is this a reMarkable .lines file?
        expected_header=b'reMarkable lines with selections and layers'
        if len(data) < len(expected_header) + 4:
            abort('File too short to be a valid file')

        fmt = '<{}sI'.format(len(expected_header))
        header, npages = struct.unpack_from(fmt, data, offset); offset += struct.calcsize(fmt)
        if header != expected_header or npages < 1:
            abort('Not a valid reMarkable file: <header={}><npages={}>'.format(header, npages))

        output.write(
            '<svg xmlns="http://www.w3.org/2000/svg" height="{}" width="{}">'.format(
                self.y_width, self.x_width
            )
        ) # BEGIN Notebook
        output.write('''
            <script type="application/ecmascript"> <![CDATA[
                var visiblePage = 'p0';
                function goToPage(page) {
                    document.getElementById(visiblePage).setAttribute('style', 'display: none');
                    document.getElementById(page).setAttribute('style', 'display: inline');
                    visiblePage = page;
                }
            ]]> </script>
        ''')

        # Iterate through pages (there is at least one)
        for page in range(npages):
            # BEGIN page
            # Opening page group, visible only for the first page.
            output.write('<g id="p{}" style="display:{}">'.format(page, 'none' if page != 0 else 'inline'))

            fmt = '<BBH' # TODO might be 'I'
            nlayers, b_unk, h_unk = struct.unpack_from(fmt, data, offset); offset += struct.calcsize(fmt)
            if b_unk != 0 or h_unk != 0: # Might indicate which layers are visible.
                print('Unexpected value on page {} after nlayers'.format(page + 1))

            # Iterate through layers on the page (there is at least one)
            for layer in range(nlayers):
                fmt = '<I'
                (nstrokes,) = struct.unpack_from(fmt, data, offset); offset += struct.calcsize(fmt)

                # Iterate through the strokes in the layer (if there is any)
                for stroke in range(nstrokes):
                    fmt = '<IIIfI'
                    pen, color, i_unk, width, nsegments = struct.unpack_from(fmt, data, offset); offset += struct.calcsize(fmt)
                    opacity = 1
                    last_x = -1.; last_y = -1.
                    #if i_unk != 0: # No theory on that one
                        #print('Unexpected value at offset {}'.format(offset - 12))
                    if pen == 0 or pen == 1:
                        pass # Dynamic width, will be truncated into several strokes
                    elif pen == 2 or pen == 4: # Pen / Fineliner
                        width = 32 * width * width - 116 * width + 107
                    elif pen == 3: # Marker
                        width = 64 * width - 112
                        opacity = 0.9
                    elif pen == 5: # Highlighter
                        width = 30
                        opacity = 0.2
                        if colored:
                            color = 3
                    elif pen == 6: # Eraser
                        width = 1280 * width * width - 4800 * width + 4510
                        color = 2
                    elif pen == 7: # Pencil-Sharp
                        width = 16 * width - 27
                        opacity = 0.9
                    elif pen == 8: # Erase area
                        opacity = 0.
                    else:
                        print('Unknown pen: {}'.format(pen))
                        opacity = 0.

                    output.write('<polyline style="fill:none;stroke:{};stroke-width:{:.3f};opacity:{}" points="'.format(
                        self.stroke_color[color], width, opacity)
                    ) # BEGIN stroke

                    # Iterate through the segments to form a polyline
                    for segment in range(nsegments):
                        fmt = '<fffff'
                        xpos, ypos, pressure, tilt, i_unk2 = struct.unpack_from(fmt, data, offset); offset += struct.calcsize(fmt)
                        if pen == 0:
                            if 0 == segment % 8:
                                segment_width = (5. * tilt) * (6. * width - 10) * (1 + 2. * pressure * pressure * pressure)
                                output.write('" /><polyline style="fill:none;stroke:{};stroke-width:{:.3f}" points="'.format(
                                            self.stroke_color[color], segment_width)
                                ) # UPDATE stroke
                                if last_x != -1.:
                                    output.write('{:.3f},{:.3f} '.format(last_x, last_y)) # Join to previous segment
                                last_x = xpos; last_y = ypos
                        elif pen == 1:
                            if 0 == segment % 8:
                                segment_width = (10. * tilt -2) * (8. * width - 14)
                                segment_opacity = (pressure - .2) * (pressure - .2)
                                output.write('" /><polyline style="fill:none;stroke:{};stroke-width:{:.3f};opacity:{:.3f}" points="'.format(
                                            self.stroke_color[color], segment_width, segment_opacity)
                                ) # UPDATE stroke
                                if last_x != -1.:
                                    output.write('{:.3f},{:.3f} '.format(last_x, last_y)) # Join to previous segment
                                last_x = xpos; last_y = ypos

                        output.write('{:.3f},{:.3f} '.format(xpos, ypos)) # BEGIN and END polyline segment

                    output.write('" />\n') # END stroke

            # Overlay the page with a clickable rect to flip pages
            output.write('<rect x="0" y="0" width="{}" height="{}" fill-opacity="0" onclick="goToPage(\'p{}\')" />'.format(
                self.x_width, self.y_width, (page + 1) % npages)
            )
            output.write('</g>') # Closing page group

        output.write('</svg>') # END notebook
        output.close()
