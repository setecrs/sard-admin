import React, { useState } from 'react';

const iped_vars = `iped_locale=pt-BR
iped_tskJarPath=/usr/share/java/sleuthkit-4.9.0.jar
iped_enableOCR=false
iped_enableGraphGeneration=false
iped_robustImageReading=true
iped_useNIOFSDirectory=true
iped_numThreads=
iped_indexTemp=
iped_indexTempOnSSD=
iped_outputOnSSD=
iped_kffDb=
iped_ledWkffPath=
iped_photoDNAHashDatabase=
iped_ledDie=
iped_mplayerPath=
iped_optional_jars=
iped_regripperFolder=
iped_hash=
iped_enablePhotoDNA=
iped_enableKff=
iped_enableLedWkff=
iped_enableLedDie=
iped_excludeKffIgnorable=
iped_ignoreDuplicates=
iped_exportFileProps=
iped_processFileSignatures=
iped_enableFileParsing=
iped_expandContainers=
iped_enableRegexSearch=
iped_enableLanguageDetect=
iped_enableNamedEntityRecogniton=
iped_indexFileContents=
iped_indexUnknownFiles=
iped_indexCorruptedFiles=
iped_enableAudioTranscription=
iped_addFileSlacks=
iped_addUnallocated=
iped_indexUnallocated=
iped_enableCarving=
iped_enableKFFCarving=
iped_enableKnownMetCarving=
iped_enableImageThumbs=
iped_enableImageSimilarity=
iped_enableVideoThumbs=
iped_enableHTMLReport=
iped_numImageReaders=
iped_enableExternalParsing=
iped_numExternalParsers=
iped_externalParsingMaxMem=
iped_phoneParsersToUse=
iped_forceMerge=
iped_timeOut=
iped_timeOutPerMB=
iped_embutirLibreOffice=
iped_sortPDFChars=
iped_entropyTest=
iped_minRawStringSize=
iped_extraCharsToIndex=
iped_convertCharsToLowerCase=
iped_filterNonLatinChars=
iped_convertCharsToAscii=
iped_ignoreHardLinks=
iped_minOrphanSizeToIgnore=
iped_unallocatedFragSize=
iped_minItemSizeToFragment=
iped_textSplitSize=
iped_commitIntervalSeconds=
iped_OCRLanguage=
iped_pageSegMode=
iped_minFileSize2OCR=
iped_maxFileSize2OCR=
iped_pdfToImgResolution=
iped_maxPDFTextSize2OCR=
iped_pdfToImgLib=
iped_externalPdfToImgConv=
iped_externalConvMaxMem=
iped_processImagesInPDFs=
iped_searchThreads=
iped_maxBackups=
iped_backupInterval=
iped_autoManageCols=
iped_preOpenImagesOnSleuth=
iped_openImagesCacheWarmUpEnabled=
iped_openImagesCacheWarmUpThreads=`

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

