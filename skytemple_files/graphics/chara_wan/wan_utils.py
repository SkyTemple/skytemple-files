#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
# mypy: ignore-errors

from __future__ import annotations

from skytemple_files.graphics.chara_wan.model import (
    FrameOffset,
    ImgPiece,
    MetaFramePiece,
    SequenceFrame, MINUS_FRAME,
)


def animGroupsEqual(anim1, anim2):
    if len(anim1) != len(anim2):
        return False

    anims_equal = True
    # perform a check to see if they're equal
    for anim_idx in range(len(anim1)):
        if len(anim1[anim_idx]) != len(anim2[anim_idx]):
            anims_equal = False
            break

        for frame_idx in range(len(anim1[anim_idx])):
            frame1 = anim1[anim_idx][frame_idx]
            frame2 = anim2[anim_idx][frame_idx]

            if (
                frame1.frameIndex != frame2.frameIndex
                or frame1.duration != frame2.duration
                or frame1.offset != frame2.offset
                or frame1.shadow != frame2.shadow
            ):
                anims_equal = False
                break
        if not anims_equal:
            break
    return anims_equal


def duplicateAnimGroup(anim):
    new_group = []
    for anim_seq in anim:
        new_seq = []
        for frame in anim_seq:
            new_frame = SequenceFrame(frame.frameIndex, frame.duration, frame.flag, frame.offset, frame.shadow)
            new_frame.SetRushPoint(frame.IsRushPoint())
            new_seq.append(new_frame)
        new_group.append(new_seq)
    return new_group


def duplicateMetaFrame(frame):
    new_frame = []
    for piece in frame:
        new_piece = MetaFramePiece(piece.imgIndex, piece.attr0, piece.attr1, piece.attr2)
        new_frame.append(new_piece)
    return new_frame


def duplicateOffset(offset):
    return FrameOffset(offset.head, offset.lhand, offset.rhand, offset.center)


def duplicateImgData(imgStrip):
    new_img = ImgPiece()
    new_img.zSort = imgStrip.zSort
    for strip in imgStrip.imgPx:
        new_strip = strip.copy()
        new_img.imgPx.append(new_strip)

    return new_img


def mapImgData(inputImgData, imgData, frameData):
    mapping = {}
    for idx, img in enumerate(inputImgData):
        dupe_idx = -1
        for check_idx, check_img in enumerate(imgData):
            imgs_equal = True
            # perform a check to see if they're equal
            if len(img.imgPx) == len(check_img.imgPx):
                for ii in range(len(img.imgPx)):
                    if len(img.imgPx[ii]) == len(check_img.imgPx[ii]):
                        for jj in range(len(img.imgPx[ii])):
                            if img.imgPx[ii][jj] != check_img.imgPx[ii][jj]:
                                imgs_equal = False
                                break
                    else:
                        imgs_equal = False

                    if not imgs_equal:
                        break
            else:
                imgs_equal = False

            if imgs_equal:
                dupe_idx = check_idx
                break
        if dupe_idx > -1:
            mapping[idx] = dupe_idx
        else:
            mapping[idx] = len(imgData)
            imgData.append(img)

    for frame in frameData:
        for piece in frame:
            if piece.imgIndex != MINUS_FRAME:
                piece.imgIndex = mapping[piece.imgIndex]