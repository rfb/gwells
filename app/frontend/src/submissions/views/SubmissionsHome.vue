<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">
        <b-row>
          <b-col lg="8">Well Activity Submission</b-col>
          <b-col lg="4" class="text-right">
            <b-btn size="sm" :variant="`${formIsFlat ? 'primary':'outline-primary'}`" @click="formIsFlat=true">Flat form</b-btn>
            <b-btn size="sm" :variant="`${formIsFlat ? 'outline-primary':'primary'}`" @click="formIsFlat=false">Wizard</b-btn>
          </b-col>
        </b-row>
      </h4>
      <p>Submit activity on a well. <a href="/gwells/">Try a search</a> to see if the well exists in the system before submitting a report.</p>

      <!-- Activity submission form -->
      <b-form @submit.prevent="confirmSubmit">

        <!-- Form load/save -->
        <b-row>
          <b-col class="text-right">
            <b-btn size="sm" variant="outline-primary" @click="saveForm">
              Save
              <transition name="bounce" mode="out-in">
                  <i v-show="saveFormSuccess" class="fa fa-check text-success"></i>
              </transition>
            </b-btn>
            <b-btn size="sm" variant="outline-primary" @click="loadConfirmation" ref="confirmLoadBtn">
              Load
              <transition name="bounce">
                  <i v-show="loadFormSuccess" class="fa fa-check text-success"></i>
              </transition>
            </b-btn>
          </b-col>
        </b-row>

        <!-- Form step 1: Type of well -->
        <step01-type class="my-3"
          v-if="formStep === 1 || formIsFlat"
          :wellTagNumber.sync="form.well"
          :wellActivityType.sync="form.well_activity_type"
          :wellClass.sync="form.well_class"
          :wellSubclass.sync="form.well_subclass"
          :intendedWaterUse.sync="form.intended_water_use"
          :units.sync="units"
          :personResponsible.sync="form.driller_responsible"
          :idPlateNumber.sync="form.identification_plate_number"
          :wellPlateAttached.sync="form.well_plate_attached"
          :drillerName.sync="form.driller_name"
          :consultantName.sync="form.consultant_name"
          :consultantCompany.sync="form.consultant_company"
          :workStartDate.sync="form.work_start_date"
          :workEndDate.sync="form.work_end_date"
          :drillerSameAsPersonResponsible.sync="form.meta.drillerSameAsPersonResponsible"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        ></step01-type>

        <!-- Step 2: Owner information -->
        <step02-owner class="my-3"
          v-if="formStep === 2 || formIsFlat"
          :ownerFullName.sync="form.owner_full_name"
          :ownerMailingAddress.sync="form.owner_mailing_address"
          :ownerProvinceState.sync="form.owner_province_state"
          :ownerCity.sync="form.owner_city"
          :ownerPostalCode.sync="form.owner_postal_code"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        ></step02-owner>

        <!-- Step 3: Well location -->
        <step03-location class="my-3"
          v-if="formStep === 3 || formIsFlat"
          :streetAddress.sync="form.street_address"
          :city.sync="form.city"
          :legalLot.sync="form.legal_lot"
          :legalPlan.sync="form.legal_plan"
          :legalDistrictLot.sync="form.legal_district_lot"
          :legalBlock.sync="form.legal_block"
          :legalSection.sync="form.legal_section"
          :legalTownship.sync="form.legal_township"
          :legalRange.sync="form.legal_range"
          :landDistrict.sync="form.land_district"
          :legalPID.sync="form.legal_pid"
          :wellLocationDescription.sync="form.well_location_description"
        ></step03-location>

        <!-- Step 4: Coords and Method of Drilling -->
        <step04-coords class="my-3"
          v-if="formStep === 4 || formIsFlat"
          :latitude.sync="form.latitude"
          :longitude.sync="form.longitude"
          :groundElevation.sync="form.ground_elevation"
          :groundElevationMethod.sync="form.ground_elevation_method"
          :drillingMethod.sync="form.drilling_method"
          :otherDrillingMethod.sync="form.other_drilling_method"
          :wellOrientation.sync="form.well_orientation"
          >
        </step04-coords>

        <!-- Step 5: Lithology -->
        <step05-lithology class="my-3"
          v-if="formStep === 5 || formIsFlat"
          :lithology.sync="form.lithology_set"
        ></step05-lithology>

        <!-- Step 6: Casings -->
        <step06-casings class="my-3"
          v-if="formStep === 6 || formIsFlat"
          :casings.sync="form.casing_set"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
          />

        <!-- Step 7: Surface Seal / Backfill Material -->
        <step07-backfill class="my-3"
          v-if="formStep === 7 || formIsFlat"
          :surfaceSealMaterial.sync="form.surface_seal_material"
          :surfaceSealDepth.sync="form.surface_seal_depth"
          :surfaceSealThickness.sync="form.surface_seal_thickness"
          :surfaceSealMethod.sync="form.surface_seal_method"
          :backfillAboveSurfaceSeal.sync="form.backfill_above_surface_seal"
          :backfillDepth.sync="form.backfill_above_surface_seal_depth"
        ></step07-backfill>

        <!-- Liner Information -->
        <liner class="my-3"
          v-if="formStep === 8 || formIsFlat"
          :linerMaterial.sync="form.liner_material"
          :linerDiameter.sync="form.liner_diameter"
          :linerThickness.sync="form.liner_thickness"
          :linerFrom.sync="form.liner_from"
          :linerTo.sync="form.liner_to"
          :linerPerforations.sync="form.linerperforation_set"
          :errors="errors"
          :fieldsLoaded="fieldsLoaded"
        />

        <!-- Step 9: Screens -->
        <step09-screens class="my-3"
          v-if="formStep === 9 || formIsFlat"
          :screenIntakeMethod.sync="form.screen_intake_method"
          :screenType.sync="form.screen_type"
          :screenMaterial.sync="form.screen_material"
          :otherScreenMaterial.sync="form.other_screen_material"
          :screenOpening.sync="form.screen_opening"
          :screenBottom.sync="form.screen_bottom"
          :screens.sync="form.screen_set"
        ></step09-screens>

        <!-- Step 10: Filter Pack -->
        <step10-filterPack class="my-3"
          v-if="formStep === 10 || formIsFlat"
          :filterPackFrom.sync="form.filter_pack_from"
          :filterPackTo.sync="form.filter_pack_to"
          :filterPackThickness.sync="form.filter_pack_thickness"
          :filterPackMaterial.sync="form.filter_pack_material"
          :filterPackMaterialSize.sync="form.filter_pack_material_size"
        />

        <!-- Step 11: Well Development -->
        <step11-development class="my-3"
          v-if="formStep === 11 || formIsFlat"
          :developmentMethod.sync="form.development_method"
          :developmentHours.sync="form.development_hours"
          :developmentNotes.sync="form.development_notes"
        ></step11-development>

        <!-- Step 12: Yield (Production Data) -->
        <step12-yield class="my-3"
          v-if="formStep === 12 || formIsFlat"
          :productionData.sync="form.production_data_set"
        ></step12-yield>

        <!-- Step 13: Water Quality -->
        <step13-water-quality class="my-3"
          v-if="formStep === 13 || formIsFlat"
          :waterQualityCharacteristics.sync="form.water_quality_characteristics"
          :waterQualityColour.sync="form.water_quality_colour"
          :waterQualityOdour.sync="form.water_quality_odour"
          :emsID.sync="form.ems_id"
        ></step13-water-quality>

        <step14-completion class="my-3"
          v-if="formStep === 14 || formIsFlat"
          :totalDepthDrilled.sync="form.total_depth_drilled"
          :finishedWellDepth.sync="form.finished_well_depth"
          :finalCasingStickUp.sync="form.final_casing_stick_up"
          :bedrockDepth.sync="form.bedrock_depth"
          :staticWaterLevel.sync="form.static_water_level"
          :wellYield.sync="form.well_yield"
          :artesianFlow.sync="form.artesian_flow"
          :artesianPressure.sync="form.artesian_pressure"
          :wellCapType.sync="form.well_cap_type"
          :wellDisinfected.sync="form.well_disinfected"
        ></step14-completion>

        <step15-comments class="my-3"
          v-if="formStep === 15 || formIsFlat"
          :comments.sync="form.comments"
          :alternativeSpecsSubmitted.sync="form.alternative_specs_submitted"
        ></step15-comments>

        <!-- Back / Next / Submit controls -->
        <b-row class="mt-5">
          <b-col v-if="!formIsFlat">
            <b-btn v-if="step > 1" @click="step > 1 ? step-- : null">Back</b-btn>
          </b-col>
          <b-col :class="`pr-4 ${formIsFlat ? '':'text-right'}`">
            <b-btn v-if="step < maxSteps && !formIsFlat" @click="step++">Next</b-btn>
            <b-btn v-else id="formSubmitButton" type="submit" variant="primary" ref="activitySubmitBtn" :disabled="formSubmitLoading">Submit</b-btn>
          </b-col>
        </b-row>
      </b-form>

      <!-- Form submission success message -->
      <b-alert
          :show="formSubmitSuccess"
          dismissible
          @dismissed="formSubmitSuccess=false"
          variant="success"
          class="mt-3">Report submitted!</b-alert>

      <!-- Form submission error message -->
      <b-alert
          :show="formSubmitError"
          dismissible
          @dismissed="formSubmitError=false"
          variant="danger"
          class="mt-3">
        <span v-if="errors && errors.detail">
          {{ errors.detail }}
        </span>
        <div v-if="errors && errors != {}">
          <div v-for="(field, i) in Object.keys(errors)" :key="`submissionError${i}`">
            {{field | readable}} : <span v-for="(e, j) in errors[field]" :key="`submissionError${i}-${j}`">{{ e }}</span>
          </div>
        </div>
        </b-alert>

      <!-- Form submission confirmation -->
      <b-modal
          v-model="confirmSubmitModal"
          id="confirmSubmitModal"
          centered
          title="Confirm submission"
          @shown="$refs.confirmSubmitConfirmBtn.focus()"
          :return-focus="$refs.activitySubmitBtn">
        Are you sure you want to submit this activity report?
        <div slot="modal-footer">
          <b-btn variant="primary" @click="confirmSubmitModal=false;formSubmit()" ref="confirmSubmitConfirmBtn">
            Save
          </b-btn>
          <b-btn variant="light" @click="confirmSubmitModal=false">
            Cancel
          </b-btn>
        </div>
      </b-modal>

      <!-- Form reload (load from save) confirmation -->
      <b-modal
          v-model="confirmLoadModal"
          centered
          title="Confirm load submission data"
          @shown="$refs.confirmLoadConfirmBtn.focus()"
          :return-focus="$refs.loadFormBtn">
        Are you sure you want to load the previously saved activity report? Your current report will be overwritten.
        <div slot="modal-footer">
          <b-btn variant="primary" @click="confirmLoadModal=false;loadForm()" ref="confirmLoadConfirmBtn">
            Load
          </b-btn>
          <b-btn variant="light" @click="confirmLoadModal=false">
            Cancel
          </b-btn>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import ApiService from '@/common/services/ApiService.js'
import { FETCH_CODES } from '../store/actions.types.js'
import inputFormatMixin from '@/common/inputFormatMixin.js'
import Step01Type from '@/submissions/components/SubmissionForm/Step01Type.vue'
import Step02Owner from '@/submissions/components/SubmissionForm/Step02Owner.vue'
import Step03Location from '@/submissions/components/SubmissionForm/Step03Location.vue'
import Step04Coords from '@/submissions/components/SubmissionForm/Step04Coords.vue'
import Step05Lithology from '@/submissions/components/SubmissionForm/Step05Lithology.vue'
import Step06Casings from '@/submissions/components/SubmissionForm/Step06Casings.vue'
import Step07Backfill from '@/submissions/components/SubmissionForm/Step07Backfill.vue'
import Liner from '@/submissions/components/SubmissionForm/Liner.vue'
import Step09Screens from '@/submissions/components/SubmissionForm/Step09Screens.vue'
import Step10FilterPack from '@/submissions/components/SubmissionForm/Step10FilterPack.vue'
import Step11Development from '@/submissions/components/SubmissionForm/Step11Development.vue'
import Step12Yield from '@/submissions/components/SubmissionForm/Step12Yield.vue'
import Step13WaterQuality from '@/submissions/components/SubmissionForm/Step13WaterQuality.vue'
import Step14Completion from '@/submissions/components/SubmissionForm/Step14Completion.vue'
import Step15Comments from '@/submissions/components/SubmissionForm/Step15Comments.vue'
export default {
  name: 'SubmissionsHome',
  mixins: [inputFormatMixin],
  components: {
    Step01Type,
    Step02Owner,
    Step03Location,
    Step04Coords,
    Step05Lithology,
    Step06Casings,
    Step07Backfill,
    Liner,
    Step09Screens,
    Step10FilterPack,
    Step11Development,
    Step12Yield,
    Step13WaterQuality,
    Step14Completion,
    Step15Comments
  },
  data () {
    return {
      formIsFlat: true,
      units: 'imperial',
      confirmSubmitModal: false,
      formSubmitLoading: false,
      formSubmitSuccess: false,
      formSubmitError: false,
      saveFormSuccess: false,
      loadFormSuccess: false,
      confirmLoadModal: false,
      step: 1,
      maxSteps: 15, // total number of wizard steps
      sliding: null,
      errors: {},
      fieldsLoaded: {},
      form: {},
      formOptions: {}
    }
  },
  computed: {
    formStep () {
      return (this.step % (this.maxSteps + 1))
    }
  },
  methods: {
    formSubmit () {
      const data = Object.assign({}, this.form)

      // delete "meta" data (form input that need not be submitted) stored within form object
      delete data.meta

      // replace the "person responsible" object with the person's guid
      if (data.driller_responsible && data.driller_responsible.person_guid) {
        data.driller_responsible = data.driller_responsible.person_guid
      }

      if (data.well && data.well.well_tag_number) {
        data.well = data.well.well_tag_number
      }

      this.stripBlankStrings(data)

      this.formSubmitLoading = true
      this.formSubmitSuccess = false
      this.formSubmitError = false
      this.errors = {}
      ApiService.post('submissions', data).then(() => {
        this.formSubmitSuccess = true
        this.resetForm()
      }).catch((error) => {
        this.errors = error.response.data
        this.formSubmitError = true
      }).finally(() => {
        this.formSubmitLoading = false
      })
    },
    confirmSubmit () {
      this.confirmSubmitModal = true
    },
    resetForm () {
      this.form = {
        well_activity_type: 'CON',
        well: null,
        well_class: '',
        well_subclass: '',
        intended_water_use: '',
        identification_plate_number: null,
        well_plate_attached: '',
        driller_responsible: null,
        driller_name: '',
        consultant_name: '',
        consultant_company: '',
        work_start_date: '',
        work_end_date: '',
        owner_full_name: '',
        owner_mailing_address: '',
        owner_city: '',
        owner_province_state: '',
        owner_postal_code: '',
        street_address: '', // this is the street address of the well location
        city: '', // well location city
        legal_lot: '',
        legal_plan: '',
        legal_district_lot: '',
        legal_block: '',
        legal_section: '',
        legal_township: '',
        legal_range: '',
        land_district: '',
        legal_pid: '',
        liner_material: null,
        liner_diameter: null,
        liner_thickness: null,
        liner_from: null,
        liner_to: null,
        linerperforation_set: [{}, {}, {}],
        well_location_description: '',
        latitude: '',
        longitude: '',
        ground_elevation: null,
        ground_elevation_method: '',
        drilling_method: '',
        well_orientation: '',
        lithology_set: [],
        surface_seal_material: '',
        surface_seal_depth: '',
        surface_seal_thickness: '',
        surface_seal_method: '',
        backfill_above_surface_seal: '',
        backfill_above_surface_seal_depth: '',
        casing_set: [{}, {}, {}],
        screen_intake_method: '',
        screen_type: '',
        screen_material: '',
        other_screen_material: '',
        screen_opening: '',
        screen_bottom: '',
        screen_set: [],
        development_method: '',
        development_hours: '',
        development_notes: '',
        production_data_set: [],
        filter_pack_from: '',
        filter_pack_to: '',
        filter_pack_thickness: '',
        filter_pack_material: '',
        filter_pack_material_size: '',
        water_quality_characteristics: [],
        water_quality_colour: '',
        water_quality_odour: '',
        ems_id: '',
        total_depth_drilled: '',
        finished_well_depth: '',
        final_casing_stick_up: '',
        bedrock_depth: '',
        static_water_level: '',
        well_yield: '',
        artesian_flow: '',
        artesian_pressure: '',
        well_cap_type: '',
        well_disinfected: 'False',
        comments: '',
        alternative_specs_submitted: 'False',

        // non-form fields that should be saved with form
        meta: {
          drillerSameAsPersonResponsible: false
        }
      }
    },
    saveForm () {
      // saves a copy of form data locally
      this.saveStatusReset()
      const data = JSON.stringify(this.form)
      localStorage.setItem('savedFormData', data)
      setTimeout(() => { this.saveFormSuccess = true }, 10)
      setTimeout(() => { this.saveFormSuccess = false }, 1000)
    },
    loadForm () {
      this.saveStatusReset()
      const storedData = localStorage.getItem('savedFormData')
      if (storedData) {
        this.resetForm()

        // some form features depend on watching form field values.
        // setTimeout pushes rendering new data down execution queue
        // to give watchers a chance to act on each set of changes
        // (e.g. form reset, form population)
        setTimeout(() => {
          const parsedData = JSON.parse(storedData)
          this.form = Object.assign(this.form, parsedData)
          this.fieldsLoaded = Object.assign(this.fieldsLoaded, parsedData)
          setTimeout(() => { this.loadFormSuccess = true }, 0)
          setTimeout(() => { this.fieldsLoaded = {} }, 0)
          setTimeout(() => { this.loadFormSuccess = false }, 1000)
        }, 0)
      }
    },
    loadConfirmation () {
      this.confirmLoadModal = true
    },
    saveStatusReset () {
      this.saveFormSuccess = false
      this.loadFormSuccess = false
    },
    setWellTagNumber (well) {
      // setWellTagNumber is used to link an activity report to a well other than through the dropdown menu.
      // the dropdown menu returns an object so this method also does.
      this.form.well = { well_tag_number: well }
    },
    stripBlankStrings (formObject) {
      // strips blank strings from a form object

      Object.keys(formObject).forEach((key) => {
        if (typeof formObject[key] === 'object' && formObject[key] !== null) {
          // descend into nested objects
          this.stripBlankStrings(formObject[key])
        }

        if (formObject[key] === '') {
          delete formObject[key]
        }
      })
    }
  },
  watch: {
    form: {
      handler () {
        this.saveStatusReset()
      },
      deep: true
    }
  },
  created () {
    this.resetForm()
    this.$store.dispatch(FETCH_CODES)

    if (this.$route.params.id) {
      this.setWellTagNumber(this.$route.params.id)
    }
    if (this.$route.name === 'SubmissionsEdit') {
      this.form.well_activity_type = 'STAFF_EDIT'
    }
  }
}
</script>

<style lang="scss">
.slide-leave-active,
.slide-enter-active {
  transition: 1s;
}
.slide-enter {
  transform: translate(100%, 0);
}
.slide-leave-to {
  transform: translate(-100%, 0);
}
.bounce-enter-active {
  animation: bounce-in .5s;
}
.bounce-leave-active {
  animation: bounce-out .2s;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes bounce-out {
  100% {
    transform: scale(0)
  }
}
.input-width-small {
  max-width: 5rem;
}
.input-width-medium {
  max-width: 10rem;
}
</style>
