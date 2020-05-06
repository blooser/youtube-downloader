import QtQuick 2.14

ListModel {

    ListElement {
        format: "webm"
        type: "Video + Audio"
        description: "WebM is an audiovisual media file format. It is primarily intended to offer a royalty-free alternative to use in the HTML5 video and the HTML5 audio elements. It has a sister project WebP for images. The development of the format is sponsored by Google, and the corresponding software is distributed under a BSD license. "
        readMore: "https://en.wikipedia.org/wiki/WebM"
    }

    ListElement {
        format: "mp4"
        type: "Video + Audio"
        description: "Digital multimedia container format most commonly used to store video and audio, but it can also be used to store other data such as subtitles and still images. Like most modern container formats, it allows streaming over the Internet. The only official filename extension for MPEG-4 Part 14 files is .mp4. MPEG-4 Part 14 (formally ISO/IEC 14496-14:2003) is a standard specified as a part of MPEG-4. "
        readMore: "https://en.wikipedia.org/wiki/MPEG-4_Part_14"
    }

    ListElement {
        format: "mkv"
        type: "Video + Audio"
        description: "Free, open-standard container format, a file format that can hold an unlimited number of video, audio, picture, or subtitle tracks in one file. It is a universal format for storing common multimedia content, like movies or TV shows. Matroska is similar in concept to other containers like AVI, MP4, or Advanced Systems Format (ASF), but is entirely open in specification, with implementations consisting mostly of open source software. Matroska file extensions are .MKV for video (which may or may not include subtitles and audio), .MK3D for stereoscopic video, .MKA for audio-only files, and .MKS for subtitles only."
        readMore: "https://en.wikipedia.org/wiki/Matroska"
    }

    ListElement {
        format: "m4a"
        type: "Audio"
        description: "Audio file, which is a MPEG-4 Part 14 container containing AAC-encoded audio."
        readMore: "https://en.wikipedia.org/wiki/MPEG-4_Part_14"
    }

    ListElement {
        format: "mp3"
        type: "Audio"
        description: "File format commonly designates files containing an elementary stream of MPEG-1 Audio or MPEG-2 Audio encoded data, without other complexities of the MP3 standard. MP3 uses lossy data-compression to encode data using inexact approximations and the partial discarding of data. This allows a large reduction in file sizes when compared to uncompressed audio. The combination of small size and acceptable fidelity led to a boom in the distribution of music over the Internet in the mid- to late-1990s, with MP3 serving as an enabling technology at a time when bandwidth and storage were still at a premium. The MP3 format soon became associated with controversies surrounding copyright infringement, music piracy, and the file ripping/sharing services MP3.com and Napster, among others. With the advent of portable media players, a product category also including smartphones, MP3 support remains near-universal. "
        readMore: "https://en.wikipedia.org/wiki/MP3"
    }

    ListElement {
        format: "flac"
        type: "Audio"
        description: "Audio coding format for lossless compression of digital audio, and is also the name of the free software project producing the FLAC tools, the reference software package that includes a codec implementation. Digital audio compressed by FLAC's algorithm can typically be reduced to between 50 and 70 percent of its original size and decompress to an identical copy of the original audio data. "
        readMore: "https://en.wikipedia.org/wiki/FLAC"
    }

    ListElement {
        format: "wav"
        type: "Audio"
        description: "Audio file format standard, developed by Microsoft and IBM, for storing an audio bitstream on PCs. It is an application of the Resource Interchange File Format (RIFF) bitstream format method for storing data in 'chunks', and thus is also close to the 8SVX and the AIFF format used on Amiga and Macintosh computers, respectively. It is the main format used on Microsoft Windows systems for raw and typically uncompressed audio. The usual bitstream encoding is the linear pulse-code modulation (LPCM) format."
        readMore: "https://en.wikipedia.org/wiki/WAV"
    }
}
