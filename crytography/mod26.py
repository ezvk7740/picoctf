import codecs

string = "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_Ncualgvd}"
rot13 = lambda s: codecs.getencoder("rot-13")(s)[0]
print(rot13(string))
