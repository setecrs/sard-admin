import React, { useState } from 'react';

const iped_vars = `iped_locale=pt-BR
iped_tskJarPath=/usr/share/java/sleuthkit-4.9.0.jar
iped_enableOCR=false
iped_enableGraphGeneration=false
iped_robustImageReading=true
iped_useNIOFSDirectory=true
iped_numThreads=12
iped_indexTemp=/mnt/ipedtmp
iped_indexTempOnSSD=true
iped_outputOnSSD=false
iped_kffDb=/mnt/kff/kff.db
iped_ledWkffPath=/mnt/led/pedo/wkff
iped_photoDNAHashDatabase=/mnt/PhotoDNA/PhotoDNAChildPornHashes.txt
iped_ledDie=/mnt/led/pedo/die/rfdie.dat
iped_mplayerPath=/usr/bin/mplayer
iped_optional_jars=../optional_jars/
iped_regripperFolder=../regripper/
iped_hash=
iped_enablePhotoDNA=true
iped_enableKff=true
iped_enableLedWkff=true
iped_enableLedDie=true
iped_excludeKffIgnorable=false
iped_ignoreDuplicates=false
iped_exportFileProps=true
iped_processFileSignatures=true
iped_enableFileParsing=true
iped_expandContainers=true
iped_enableRegexSearch=true
iped_enableLanguageDetect=true
iped_enableNamedEntityRecogniton=false
iped_indexFileContents=true
iped_indexUnknownFiles=true
iped_indexCorruptedFiles=true
iped_enableAudioTranscription=
iped_addFileSlacks=true
iped_addUnallocated=true
iped_indexUnallocated=true
iped_enableCarving=true
iped_enableKFFCarving=true
iped_enableKnownMetCarving=true
iped_enableImageThumbs=true
iped_enableImageSimilarity=
iped_enableVideoThumbs=true
iped_enableHTMLReport=true
iped_numImageReaders=auto
iped_enableExternalParsing=false
iped_numExternalParsers=auto
iped_externalParsingMaxMem=512M
iped_phoneParsersToUse=internal
iped_forceMerge=false
iped_timeOut=180
iped_timeOutPerMB=2
iped_embutirLibreOffice=true
iped_sortPDFChars=false
iped_entropyTest=true
iped_minRawStringSize=4
iped_extraCharsToIndex=
iped_convertCharsToLowerCase=true
iped_filterNonLatinChars=false
iped_convertCharsToAscii=true
iped_ignoreHardLinks=true
iped_minOrphanSizeToIgnore=
iped_unallocatedFragSize=10737418240
iped_minItemSizeToFragment=104857600
iped_textSplitSize=10000000
iped_commitIntervalSeconds=
iped_OCRLanguage=por
iped_pageSegMode=1
iped_minFileSize2OCR=10000
iped_maxFileSize2OCR=100000000
iped_pdfToImgResolution=250
iped_maxPDFTextSize2OCR=100
iped_pdfToImgLib=icepdf
iped_externalPdfToImgConv=true
iped_externalConvMaxMem=512M
iped_processImagesInPDFs=true
iped_searchThreads=1
iped_maxBackups=10
iped_backupInterval=60
iped_autoManageCols=true
iped_preOpenImagesOnSleuth=false
iped_openImagesCacheWarmUpEnabled=false
iped_openImagesCacheWarmUpThreads=256`

export function LaunchPage({ iped }: {
  iped: ({
    image,
    IPEDJAR,
    EVIDENCE_PATH,
    OUTPUT_PATH,
    IPED_PROFILE,
    ADD_ARGS,
    ADD_PATHS,
    env,
  }: {
    image: string,
    IPEDJAR: string,
    EVIDENCE_PATH: string,
    OUTPUT_PATH: string,
    IPED_PROFILE: string,
    ADD_ARGS: string,
    ADD_PATHS: string,
    env: string,
  }) => Promise<void>,
}) {
  const [image, setimage] = useState('ipeddocker/iped:centos8-3.18.2')
  const [IPEDJAR, setIPEDJAR] = useState('/root/IPED/iped/iped.jar')
  const [EVIDENCE_PATH, setEVIDENCE_PATH] = useState('')
  const [OUTPUT_PATH, setOUTPUT_PATH] = useState('SARD')
  const [IPED_PROFILE, setIPED_PROFILE] = useState('forensic')
  const [ADD_ARGS, setADD_ARGS] = useState('')
  const [ADD_PATHS, setADD_PATHS] = useState('')
  const [env, setenv] = useState(iped_vars)
  const defaultBtnClass = "button btn btn-primary"
  const [btnClass, setBtnclass] = useState(defaultBtnClass)

  return <form className="form-horizontal"
    onSubmit={(e) => {
      (async () => {
        try {
          setBtnclass("button btn btn-secondary")
          await iped({
            image,
            IPEDJAR,
            EVIDENCE_PATH,
            OUTPUT_PATH,
            IPED_PROFILE,
            ADD_ARGS,
            ADD_PATHS,
            env,
          })
          setBtnclass("button btn btn-success")
        } catch (err) {
          console.error(err)
          setBtnclass("button btn btn-danger")
        }
        setTimeout(() => {
          setBtnclass(defaultBtnClass)
        }, 2000);
      })()
      e.preventDefault()
    }}
  >

    <FormItem
      value={image}
      setvalue={setimage}
      id='image'
      label='Docker image'
      placeholder='docker image'
      type='text' />
    <FormItem
      value={IPEDJAR}
      setvalue={setIPEDJAR}
      id='IPEDJAR'
      label='iped.jar full path'
      placeholder=''
      type='text' />
    <FormItem
      value={EVIDENCE_PATH}
      setvalue={setEVIDENCE_PATH}
      id='EVIDENCE_PATH'
      label='Evidence path'
      placeholder=''
      type='text' />
    <FormItem
      value={OUTPUT_PATH}
      setvalue={setOUTPUT_PATH}
      id='OUTPUT_PATH'
      label='Output path'
      placeholder=''
      type='text' />
    <FormItem
      value={IPED_PROFILE}
      setvalue={setIPED_PROFILE}
      id='IPED_PROFILE'
      label='IPED profile'
      placeholder='common options: blind default fastmode forensic pedo triage'
      type='text' />
    <FormItem
      value={ADD_ARGS}
      setvalue={setADD_ARGS}
      id='ADD_ARGS'
      label='Extra args to iped.jar'
      placeholder=''
      type='text' />
    <FormItem
      value={ADD_PATHS}
      setvalue={setADD_PATHS}
      id='ADD_PATHS'
      label='Extra evidence paths'
      placeholder=''
      type='text' />
    <div className="form-group row">
      <label htmlFor='env' className="col-md-2 col-form-label">Environment variables</label>
      <textarea
        className="form-control col-md-10"
        id='env'
        rows={8}
        placeholder=''
        value={env}
        onChange={e => {
          setenv(e.target.value)
        }}
      />
    </div>
    <div>
      <button
        type="submit"
        className={btnClass}
      >
        Launch IPED
          </button>
    </div>
  </form>
}

const FormItem = (
  { value, setvalue, id, label, placeholder, type }:
    { value: string, setvalue: Function, id: string, label: string, placeholder: string, type: string }
) =>
  <div className="form-group row">
    <label htmlFor={id} className="col-md-2 col-form-label">{label}</label>
    <input
      type={type}
      className="form-control col-md-10"
      id={id}
      placeholder={placeholder}
      value={value}
      onChange={e => {
        setvalue(e.target.value)
      }}
    />
  </div>

