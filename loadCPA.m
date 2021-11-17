function thisCPA = loadCPA(thisFile)

S = load(thisFile,'thisCPA');
thisCPA = S.thisCPA/3000;


end