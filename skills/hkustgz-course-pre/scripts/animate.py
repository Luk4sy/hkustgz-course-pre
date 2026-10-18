"""Add fade transitions, click-to-appear animations and video autoplay to a .pptx.

Usage: python animate.py in.pptx out.pptx [--video-ms 5000]

Shapes named a1_xxx, a2_xxx, ... appear on click 1, 2, ... (same number = same click).
A slide with a video and no animated shapes plays it muted on loop when the slide opens.
"""
import re, zipfile, sys, argparse
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--video-ms", type=int, default=5000, help="video length in milliseconds")
args = ap.parse_args()
src, dst = args.src, args.dst

def timing(groups, kinds):
    cid = [2]
    def nid():
        cid[0] += 1
        return cid[0]
    clicks = []
    for g in sorted(groups):
        effs = []
        for k, spid in enumerate(groups[g]):
            node = "clickEffect" if k == 0 else "withEffect"
            effs.append(
                f'<p:par><p:cTn id="{nid()}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="{node}">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                f'<p:set><p:cBhvr><p:cTn id="{nid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                f'<p:to><p:strVal val="visible"/></p:to></p:set>'
                f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{nid()}" dur="400"/>'
                f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
                f'</p:childTnLst></p:cTn></p:par>')
        outer, inner = nid(), nid()
        clicks.append(
            f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(effs) + '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    bld = "".join(f'<p:bldP spid="{sp}" grpId="0" animBg="1"/>' for g in groups for sp in groups[g] if kinds[sp] == "sp")
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            + "".join(clicks) +
            '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            '</p:childTnLst></p:cTn></p:par></p:tnLst>' + (f'<p:bldLst>{bld}</p:bldLst>' if bld else '') + '</p:timing>')


def media_timing(spid, dur_ms):
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
      '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
      '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
      '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
      '<p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
      f'<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="6" dur="{dur_ms}" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
      '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
      '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
      '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
      f'<p:video><p:cMediaNode vol="0" mute="1"><p:cTn id="7" repeatCount="indefinite" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>'
      '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')

zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
        s = data.decode("utf8")
        groups, kinds = {}, {}
        for m in re.finditer(r'<p:(sp|pic)>\s*<p:nv(?:Sp|Pic)Pr>\s*<p:cNvPr id="(\d+)" name="a(\d+)_', s):
            kind, spid, g = m.group(1), m.group(2), int(m.group(3))
            groups.setdefault(g, []).append(spid); kinds[spid] = kind
        extra = '<p:transition spd="med"><p:fade/></p:transition>'
        vm = re.search(r'<p:pic>\s*<p:nvPicPr>\s*<p:cNvPr id="(\d+)"[^>]*>(?:(?!</p:pic>).)*?<a:videoFile', s, re.S)
        if vm and not groups:
            extra += media_timing(vm.group(1), args.video_ms)
        elif groups:
            extra += timing(groups, kinds)
        assert "</p:clrMapOvr>" in s
        s = s.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + extra, 1)
        data = s.encode("utf8")
        print(item.filename, {g: len(v) for g, v in sorted(groups.items())})
    zout.writestr(item, data)
zout.close()
