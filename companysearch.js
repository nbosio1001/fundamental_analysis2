 function getCompanyHints(control, keysTyped){
            if(keysTyped && keysTyped.trim()){
                var overlay = control.parentNode.querySelector('label.overlabel');
                if(overlay && overlay.style) overlay.style.display = 'none';  //hide the overlay
                var hintsURL = 'https://efts.sec.gov/LATEST/search-index';
                var start = new Date();
                var request = new XMLHttpRequest();
                request.open('POST', hintsURL, true);
                request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                request.onload = function() {
                // 
                    if (this.status >= 200 && this.status < 400 && keysTyped==control.value) {
                        activeHintsKeys = keysTyped;
                        var data = JSON.parse(this.response);
                        console.log('round-trip execution time to '+hintsURL+ ' for "' + keysTyped + '" = '+((new Date()).getTime()-start.getTime())+' ms');
                        var hints = data.hits.hits;
                        var hintDivs = [];
                        var rgxKeysTyped = new RegExp('('+keysTyped.trim()+')','gi');
                        if(hints.length){
                            for(var h=0;h<hints.length;h++){
                                var CIK = hints[h]._id,
                                    entityName = hints[h]._source.entity,
                                    href = '/edgar/browse/?CIK='+CIK + (hints[h]._source.tickers?'&owner=exclude':'');
                                hintDivs.push('<tr class="smart-search-hint' +(autoselectFirstHint && h==0 ? ' smart-search-selected-hint' : '')
                                    + '" data="'+ entityName + ' (CIK '+formatCIK(CIK)+')"><td class="smart-search-hint-entity">'
                                    + '<a href="'+href+'">'+(entityName||'').replace(rgxKeysTyped, '<b>$1</b>')+'</a>'
                                    + '</td><td class="smart-search-hint-cik"><a href="'+href+'">' + ((' <i>CIK&nbsp;'+ formatCIK(CIK)+'</i>')||'')+'</a></td></tr>');
                            }
                            var hintsTable = hintsContainer.querySelector('table.smart-search-entity-hints');
                            hintsTable.innerHTML = hintDivs.join('');
                            for( var r=0; r< hintsTable.rows.length; r++){
                                hintsTable.rows[r].addEventListener('click', hintClick)
                            }
                            var spans = hintsContainer.querySelectorAll('div.smart-search-entity-hints span.smart-search-search-text');
                            for(var i=0; i<spans.length; i++){
                                spans[i].innerHTML=keysTyped;
                            }
                            hintsContainer.querySelector('.smart-search-edgar-full-text').setAttribute('href','/edgar/search/#/q='+encodeURIComponent(keysTyped.trim())+ '&dateRange=all&startdt=1995-06-01&enddt=2020-04-21');
                            hintsContainer.querySelector('div.smart-search-entity-hints').style.display = 'block';
                            if(waitingForHintsOnKeySubmit){
                                var selectedHint = hintsContainer.querySelector('.smart-search-selected-hint');
                                if(selectedHint){
                                    waitingForHintsOnKeySubmit = false;
                                    selectedHint.click(this);
                                }
                            }
                        } else {
                            hideCompanyHints();
                        }
                    } else {
                        console.log('error fetching from '+hintsURL+'; status '+this.status);
                    }
                };
                request.onerror = function() {
                    console.log('error connecting to '+hintsURL);
                };
                request.send(JSON.stringify({keysTyped: keysTyped, narrow: true}));
            } else {
                hideCompanyHints();
            }
            function formatCIK(unpaddedCIK){ //accept int or string and return string with padded zero
                var paddedCik = unpaddedCIK.toString();
                while(paddedCik.length<10) paddedCik = '0' + paddedCik;
                return paddedCik;
            }
            function hintClick(evt){
                this.querySelector('a').click();
            }
        }
        function searchSecGov(){
            window.location.href = 'https://secsearch.sec.gov/search?utf8=%3F&affiliate=secsearch&query='
                + encodeURIComponent(document.getElementById('company').value)
        }
        function hideCompanyHints(){
            var hintContainer = hintsContainer.querySelector('div.smart-search-entity-hints');
            hintContainer.style.display = 'none';
            hintContainer.querySelector('table.smart-search-entity-hints').innerHTML = '';  //remove the hint rows
        }
    }
