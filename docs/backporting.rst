.. Copyright 2023 Ross J. Duff MSc 
   The copyright holder licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.

`Meson version 1.1 <https://mesonbuild.com/Release-notes-for-1-1-0.html>`_

There are a number of concerns that would need to be addressed
to backport OZI to Meson 1.0 and Meson 0.X releases.

* The use of the 'in' operator on string options is not supported prior to 1.0
* The use of the 'not in' operator on string options is not supported prior to 1.0
* Support for reading options from meson.options was added in 1.1
* Use of Feature.enable_auto_if() is not supported prior to 1.1
* Use of FeatureOption.enable_if() is not supported prior to 1.1
* Use of FeatureOption.disable_if() is not supported prior to 1.1
* Use of fs.copyfile() is not supported prior to 0.64

I personally do not see much point in supporting Meson's prior versions.