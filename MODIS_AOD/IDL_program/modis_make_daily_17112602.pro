;PRO MODIS_make_daily

@MODIS_L2_AOD_READ

;; ============================================
;; * Time Domain

    smonth  = 01
    sday    = 01
    syear   = 2014
    sjul    = julday(smonth, sday, syear)

    emonth  = 12
    eday    = 31 
    eyear   = 2014
    ejul    = julday(emonth, eday, eyear)

;; ============================================
;; * PATH

	modispath   = '/media/guitar79/8T/RS_data/MODIS/DAAC_MOD04_3K/all/'
	workpath	= '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/MODIS_READ/Result_daily_050/'

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

    set_plot,'ps'
    !p.font=0 

        epsfilename = workpath + 'MODIS_AOD_daily'+yyst+julst+'.eps'

        minv = 0.0
        maxv = 2.0

        loadct,39,/silent
        device, /encapsulated, /color, bits_per_pixel = 8, filename = epsfilename, $
                /helvetica, /bold, font_size = 18, xs = 25, ys = 20
        map_set,limit = [Slat,Llon,Nlat,Rlon],color=-1 ,/isotropic,xmargin=[5,5],ymargin=[3,3]
        xyouts,0.5,0.9,'MODIS AOD'+yyst+julst,charsize=1.1,color=1,align=0.5,/normal
        loadct,33,/silent
    aodcolor = bytscl(modaod_fin,min=minv,max=maxv,top=254)

    for jj = 0, nj-2 do begin
    for ii = 0, ni-2 do begin
    if modaod_fin(ii,jj) gt -1 then begin
      xx = [lon(ii,jj),lon(ii+1,jj),lon(ii+1,jj+1),lon(ii,jj+1),lon(ii,jj)]
      yy = [lat(ii,jj),lat(ii+1,jj),lat(ii+1,jj+1),lat(ii,jj+1),lat(ii,jj)]
      polyfill,xx,yy,color=aodcolor(ii,jj),/fill
    endif
    endfor
    endfor

        cgcolorbar,position=[0.1,0.08,0.9,0.10], minrange=minv, maxrange=maxv, divisions=5, format = '(f5.2)', $
                 color = 'black', ncolors = 254,charsize=0.8

        loadct,39,/silent
        map_continents,/continents,/countries,/coast, color=0, thick=1
        map_grid,/box,latdel=5,londel=5,color=0,charsize=0.8, thick = 1
        device,/close

           ;;endelse
          ;;endfor    ;; julian date
      ;;END

              print,'====================================='
              print,'eps file is created :' + epsfilename
              print,'====================================='

      OPENW, filevar, workpath+'MODIS_AOD_daily'+yyst+julst+'.txt', /GET_LUN
          for ii=0, ni-1 do begin
          for jj=0, nj-1 do begin
          printf, filevar, Slat+del*jj, Llon+del*ii, modaod_fin(ii,jj)
      endfor
    endfor
      FREE_LUN, filevar
  
  	  print, yyst, julst
      print, '====================================='
      print, 'txt file is created :'+ workpath+'MODIS_AOD_daily'+yyst+julst+'.txt'
      print, '====================================='
		
	endelse
endfor		;; julian date
END