Various ad hoc image related utility functions and classes.

*Latest release 20240422.1*:
Updated DISTINFO.

## Function `sixel(imagepath: str) -> str`

Return the filesystem path of a cached SIXEL version of the
image at `imagepath`.

## Function `sixel_from_image_bytes(image_bs: bytes) -> str`

Return the filesystem path of a cached SIXEL version of the
image data in `image_bs`.

## Class `ThumbnailCache(cs.cache.ConvCache)`

A class to manage a collection of thumbnail images.

*Method `ThumbnailCache.create_thumbnail(self, imagepath: str, thumbpath: str, max_edge: int)`*:
Write a thumbnail image no larger than `max_edge`x`max_edge`
of `imagepath` to `thumbpath`.

*Method `ThumbnailCache.thumb_for_path(self, dx, dy, imagepath)`*:
Return the path to the thumbnail of at least `(dx,dy)` size for `imagepath`.
Creates the thumbnail if necessary.

Parameters:
* `dx`, `dy`: the target display size for the thumbnail.
* `image`: the source image, an image file pathname or a
  PIL Image instance.

The generated thumbnail will have at least these dimensions
unless either exceeds the size of the source image.
In that case the original source image will be returned;
this result can be recognised with an identity check.

Thumbnail paths are named after the SHA1 digest of their file content.

*Method `ThumbnailCache.thumb_scale(self, dx, dy)`*:
Compute thumbnail size from target dimensions.

# Release Log



*Release 20240422.1*:
Updated DISTINFO.

*Release 20240422*:
Initial PyPI release with ThumbnailCache and SIXEL functions.
