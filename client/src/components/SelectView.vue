<template>
  <div>
    <div class="form-group">
      <label for="exampleFormControlSelect1">Topic</label>
      <select class="form-control" id="exampleFormControlSelect1">
        <option>Dating</option>
        <option>Abortion</option>
        <option>Marriage</option>
      </select>
    </div>

    <div class="form-group">
      <label for="exampleFormControlInput1">Background</label>
      <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="e.g. ..." />
    </div>

    <div class="form-group">
      <label for="exampleFormControlInput1">Prefer Style</label>
      <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="e.g. ..." />
    </div>

    <div class="form-group">
      <div class="row">
        <label for="formControlRange" class="col-10">Easygoing</label>
        <label for="formControlRange">Stubborn</label>
      </div>
      <input type="range" class="form-control-range" id="formControlRange" />
    </div>

    <button type="submit" class="btn btn-primary my-1">Submit</button>
  </div>
</template>