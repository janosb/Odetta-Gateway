from odetta.models import *
from public_data.publication_list import *
from odetta.helpers.lightcurve import get_filters

def add_publication(pub_dict, models_list):
    filters = get_filters()
    new_pub, created = Publications.objects.get_or_create_publication(pub_dict)
    if created:
        new_pub.save()
    for model_specifications in models_list:
        new_model, created = PublishedModel.objects.get_or_create_published_model(
            model_specifications.get("metadata"), model_specifications.get("model_name"))
        if created:
            new_pub.publishedmodel_set.add(new_model)
        for spec_details in model_specifications.get("spectra"):
            spec, created = Spectra.objects.get_or_create_spectrum(new_model.id,
                    spec_details.get("t_expl"),
                    spec_details.get("mu"),
                    spec_details.get("phi"))
            if created:
                new_model.spectra_set.add(spec)
            flux_arr = Fluxvals.objects.filter(spectrum_id=spec.id)
            if len(flux_arr) == 0:
                print spec_details.get("specfile_rel_path")
                spec.add_fluxvals(spec_details.get("specfile_rel_path"),
                                  spec_details.get("columns", [0, 1, 2]),
                                  spec_details.get("skip_header", 0), filters)



if __name__ == "__main__":
    #print kasen2009_models
    #add_publication(kasen2009_publication, kasen2009_models)
    #add_publication(barnes2013_publication, barnes2013_models)
    add_publication(kasen2011_publication, kasen2011_models)