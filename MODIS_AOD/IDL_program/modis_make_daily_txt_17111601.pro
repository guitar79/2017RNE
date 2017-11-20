;PRO MODIS_make_daily

@MODIS_L2_AOD_READ

;;20150929
;;20160116
;; ============================================
;; * Time Domain

    smonth  = 01
    sday    = 16
    syear   = 2016
    sjul    = julday(smonth, sday, syear)

    emonth  = 12
    eday    = 31 
    eyear   = 2016
    ejul    = julday(emonth, eday, eyear)

;; ============================================
;; * PATH

	modispath   = '/media/guitar79/8T/RS_data/MODIS/DAAC_MOD04_3K/H28V05/'
	workpath	= '/home/guitar79/MODIS_READ/Result_daily_txt/'

;; ==============================================
;; * Make Grid

	  Slat = 20
    Nlat = 50
    Llon  =100
    Rlon = 150

    del = 0.5
    fac = 1./del

    ni = (Rlon-Llon)/del+1.
    nj = (Nlat-Slat)/del+1.

    lat = fltarr(ni,nj)
    lon = fltarr(ni,nj)
    for j = 0, nj-1 do lat(*,j) = Nlat-del*j
    for i = 0, ni-1 do lon(i,*) = Llon+del*i

;; ============================================
;; * READ MODIS file

for jul = sjul, ejul do begin ;;각 날짜별로 돌린다.

    caldat, jul, mm, dd, yy
    stdjul = julday(01,01,yy)
    dayn = jul-stdjul+1.

    yyst	= string(yy,'(I4.4)')
    mmst	= string(mm,'(I2.2)')
    ddst	= string(dd,'(I2.2)')
    julst	= string(dayn,'(I3.3)')

	modisname  = modispath+'MOD04_3K.A'+yyst+julst ;;파일 이름 특성상 하루 분량의 데이터를 읽게된다.
;;	file	= file_search(modispath, 'MOD04_3K.A'+yyst+julst+'*.hdf', count = modisfilen)
	file       = file_search(modisname+'*.hdf', count = modisfilen) ;;하루 치 파일을 읽음. modisfilen개이다.

	if modisfilen lt 1 then begin
    	print,'====================================='
    	print,'Cannot find MODIS L2 file:'+modisname
    	print,'====================================='
	endif else begin
	
		;; ---------------
		;; READ MODIS data
		modaod_day = fltarr(ni,nj,modisfilen) & modaod_day(*,*,*) = !values.f_nan

		for ff = 0, modisfilen-1 do begin ;;각 파일별로 for문을 돌린다.

			MODIS_L2_AOD_READ,file=file(ff),aod=modaod,lat=modlat,lon=modlon
			locidx = where(modaod gt -1 and modlat gt Slat and modlat le Nlat and modlon gt Llon and modlon le Rlon, locnum)

			if locnum lt 10 then begin
    			print,'====================================='
    			print,'Cannot find Collodated data :'+file(ff)
    			print,'====================================='
			endif else begin

				mdlat_r = round(modlat(locidx)/del)*del
				mdlon_r = round(modlon(locidx)/del)*del

				for jj = 0., nj-1 do begin
				yidx = nlat-jj*del
				ygrid = where(mdlat_r gt yidx-0.01 and mdlat_r lt yidx+0.01, ynum)
				if ynum gt 0 then begin
				
				    for ii = 0., ni-1 do begin
				        xidx = llon+ii*del
				        xgrid = where(mdlon_r(ygrid) ge xidx-0.01 and mdlon_r(ygrid) le xidx+0.01,xnum)
				        if xnum gt 0 then begin
				            data = modaod(locidx(ygrid(xgrid)))
				            dum = where(data lt 5,nanc)
				            if nanc gt fix(xnum*0.5) then begin
				                result = moment(data(dum),/nan,sdev = std)
				                if result(0) gt 0 then begin
				                modaod_day(ii,jj,ff) = result(0) ;;하루치 파일들의 셀 별 값이다.
				                endif
				            endif
				        endif
				    endfor
				
				endif
				endfor

			endelse
		endfor	;; MODIS file for a day

                modaod_fin = fltarr(ni, nj) & modaod_fin(*,*) = !values.f_nan
                for jj = 0., nj-1 do begin
                for ii = 0., ni-1 do begin
                    modaod_fin(ii,jj) = mean(modaod_day(ii,jj,*),/nan) ;;하루치 값들을 셀 별로 평균내어 하나의 array로 만든다.
                endfor
                endfor

    ;filename = workpath + 'MODIS_DayAOD'+yyst+julst+'.eps'
    OPENW, filevar, workpath + yyst+julst+'.txt', /GET_LUN
    for ii=0, ni-1 do begin
      for jj=0, nj-1 do begin
        printf, filevar, Slat+del*jj, Llon+del*ii, modaod_fin(ii,jj)
      endfor
    endfor
    FREE_LUN, filevar
      
		
		
		
		print, jul
		
		
	endelse
endfor		;; julian date
END

